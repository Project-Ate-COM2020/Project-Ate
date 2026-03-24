from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from authentication.tests import setup_random_consumer, setup_random_seller, setup_random_bundle_for_seller, \
    get_authorization_headers_for_user
from core.models import BundlePosting, Consumer, IssueReport, Reservation, Seller
from .views import ConsumerIssuesView, SellerIssuesView, SellerIssuesOverviewView, SellerIssueRespondView, \
    ConsumerCreateIssueView


class IssueReportingAPITestBase(APITestCase):
    def setUp(self):
        self.seller_user_1, self.seller_1 = setup_random_seller()
        self.seller_user_2, self.seller_2 = setup_random_seller()

        self.consumer_user_1, self.consumer_1 = setup_random_consumer()
        self.consumer_user_2, self.consumer_2 = setup_random_consumer()

        self.posting_1 = setup_random_bundle_for_seller(self.seller_1)
        self.posting_2 = setup_random_bundle_for_seller(self.seller_2)
        self.posting_3 = setup_random_bundle_for_seller(self.seller_2)

        self.consumer_user_1_headers = get_authorization_headers_for_user(self.consumer_user_1)
        self.consumer_user_2_headers = get_authorization_headers_for_user(self.consumer_user_2)

        self.seller_user_1_headers = get_authorization_headers_for_user(self.seller_user_1)
        self.seller_user_2_headers = get_authorization_headers_for_user(self.seller_user_2)

    def _create_posting(self, seller, category):
        return BundlePosting.objects.create(
            seller=seller,
            category=category,
            contents="Sample",
            quantity=10,
            quantity_remaining=10,
            price="5.00",
            pickup_window="17:00-18:00",
            status="active",
        )

    def _create_reservation(self, consumer, posting, status_value="collected", claim_code="CODE"):
        return Reservation.objects.create(
            posting=posting,
            consumer=consumer,
            claim_code=claim_code,
            status=status_value,
        )

    def _create_issue(self, posting, consumer, status_value="open", issue_type="Quality", desc="Issue"):
        return IssueReport.objects.create(
            posting=posting,
            consumer=consumer,
            type=issue_type,
            description=desc,
            status=status_value,
        )


class ConsumerCreateIssueViewTests(IssueReportingAPITestBase):
    def test_create_issue_success_for_collected_bundle(self):
        self._create_reservation(self.consumer_1, self.posting_1, "collected", "C100")
        url = reverse(ConsumerCreateIssueView.name)

        response = self.client.post(
            url,
            {
                "posting": self.posting_1.posting_id,
                "type": "Product quality",
                "description": "The bread was stale.",
            },
            format="json",
            headers=self.consumer_user_1_headers
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(IssueReport.objects.count(), 1)
        issue = IssueReport.objects.first()
        self.assertEqual(issue.status, "open")

    def test_create_issue_requires_posting(self):
        url = reverse(ConsumerCreateIssueView.name)
        response = self.client.post(
            url,
            {"type": "Product quality", "description": "Missing ids"},
            format="json",
            headers=self.consumer_user_1_headers
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_issue_rejects_when_bundle_not_reportable(self):
        self._create_reservation(self.consumer_1, self.posting_1, "expired", "C101")
        url = reverse(ConsumerCreateIssueView.name)
        response = self.client.post(
            url,
            {
                "posting": self.posting_1.posting_id,
                "type": "Product quality",
                "description": "Should fail",
            },
            format="json",
            headers=self.consumer_user_1_headers
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ConsumerIssuesViewTests(IssueReportingAPITestBase):
    def test_returns_only_selected_consumers_issues(self):
        self._create_issue(self.posting_1, self.consumer_1, desc="Mine")
        self._create_issue(self.posting_2, self.consumer_2, desc="Not mine")

        url = reverse("consumer-issues")
        response = self.client.get(url, headers=self.consumer_user_1_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["description"], "Mine")

    def test_orders_issues_by_created_at_desc(self):
        older = self._create_issue(self.posting_1, self.consumer_1, desc="Older")
        newer = self._create_issue(self.posting_2, self.consumer_1, desc="Newer")
        now = timezone.now()
        IssueReport.objects.filter(issue_id=older.issue_id).update(created_at=now - timedelta(days=2))
        IssueReport.objects.filter(issue_id=newer.issue_id).update(created_at=now - timedelta(days=1))

        url = reverse("consumer-issues")
        response = self.client.get(url, headers=self.consumer_user_1_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["issue_id"], newer.issue_id)
        self.assertEqual(response.data[1]["issue_id"], older.issue_id)

    def test_returns_empty_list_when_consumer_has_no_issues(self):
        url = reverse("consumer-issues")
        response = self.client.get(url, headers=self.consumer_user_1_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])


class ConsumerReportablePostingsViewTests(IssueReportingAPITestBase):
    def test_returns_only_reportable_postings(self):
        reservation_1 = self._create_reservation(self.consumer_1, self.posting_1, "collected", "C200")
        reservation_2 = self._create_reservation(self.consumer_1, self.posting_2, "reserved", "C201")
        self._create_reservation(self.consumer_1, self.posting_3, "expired", "C202")

        url = reverse(
            "consumer-reportable-postings",
        )
        response = self.client.get(url, headers=self.consumer_user_1_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        posting_ids = {posting["posting_id"] for posting in response.data}
        self.assertEqual(posting_ids, {self.posting_1.posting_id, self.posting_2.posting_id})
        reservation_ids = {posting["reservation_id"] for posting in response.data}
        self.assertEqual(reservation_ids, {reservation_1.reservation_id, reservation_2.reservation_id})

    def test_returns_all_reportable_reservations_for_same_posting(self):
        self._create_reservation(self.consumer_1, self.posting_1, "collected", "C210")
        self._create_reservation(self.consumer_1, self.posting_1, "collected", "C211")

        url = reverse(
            "consumer-reportable-postings",
        )
        response = self.client.get(url, headers=self.consumer_user_1_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["posting_id"], self.posting_1.posting_id)
        self.assertEqual(response.data[1]["posting_id"], self.posting_1.posting_id)

    def test_returns_empty_when_no_reportable_reservations(self):
        self._create_reservation(self.consumer_1, self.posting_1, "expired", "C220")
        url = reverse(
            "consumer-reportable-postings",
        )
        response = self.client.get(url, headers=self.consumer_user_1_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])


class SellerIssuesViewTests(IssueReportingAPITestBase):
    def test_returns_only_issues_for_given_seller(self):
        own = self._create_issue(self.posting_1, self.consumer_1, desc="Own seller")
        self._create_issue(self.posting_3, self.consumer_1, desc="Other seller")

        url = reverse(SellerIssuesView.name)
        response = self.client.get(url, headers=self.seller_user_1_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["issue_id"], own.issue_id)

    def test_returns_issues_for_non_default_seller_id(self):
        self._create_issue(self.posting_1, self.consumer_1, desc="Seller one")
        own = self._create_issue(self.posting_3, self.consumer_1, desc="Seller two")

        url = reverse(SellerIssuesView.name)
        response = self.client.get(url, headers=self.seller_user_2_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["issue_id"], own.issue_id)

    def test_orders_seller_issues_by_created_at_desc(self):
        older = self._create_issue(self.posting_1, self.consumer_1, desc="Older")
        newer = self._create_issue(self.posting_1, self.consumer_2, desc="Newer")
        now = timezone.now()
        IssueReport.objects.filter(issue_id=older.issue_id).update(created_at=now - timedelta(days=2))
        IssueReport.objects.filter(issue_id=newer.issue_id).update(created_at=now - timedelta(days=1))

        url = reverse(SellerIssuesView.name)
        response = self.client.get(url, headers=self.seller_user_1_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["issue_id"], newer.issue_id)
        self.assertEqual(response.data[1]["issue_id"], older.issue_id)

    def test_returns_empty_when_seller_has_no_issues(self):
        url = reverse(SellerIssuesView.name)
        response = self.client.get(url, headers=self.seller_user_1_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])


class SellerIssuesOverviewViewTests(IssueReportingAPITestBase):
    def test_returns_correct_status_counts(self):
        self._create_issue(self.posting_1, self.consumer_1, "open")
        self._create_issue(self.posting_1, self.consumer_1, "responded")
        self._create_issue(self.posting_1, self.consumer_1, "resolved")

        url = reverse(SellerIssuesOverviewView.name, kwargs={"seller_id": self.seller_1.pk})
        response = self.client.get(url, headers=self.seller_user_1_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_issues"], 3)
        self.assertEqual(response.data["open"], 1)
        self.assertEqual(response.data["responded"], 1)
        self.assertEqual(response.data["resolved"], 1)

    def test_counts_for_non_default_seller_id(self):
        self._create_issue(self.posting_1, self.consumer_1, "open")
        self._create_issue(self.posting_3, self.consumer_1, "responded")

        url = reverse(SellerIssuesOverviewView.name, kwargs={"seller_id": self.seller_2.pk})
        response = self.client.get(url, headers=self.seller_user_2_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_issues"], 1)
        self.assertEqual(response.data["open"], 0)
        self.assertEqual(response.data["responded"], 1)
        self.assertEqual(response.data["resolved"], 0)

    def test_unresolved_is_open_plus_responded(self):
        self._create_issue(self.posting_1, self.consumer_1, "open")
        self._create_issue(self.posting_1, self.consumer_1, "responded")
        self._create_issue(self.posting_1, self.consumer_1, "resolved")

        url = reverse(SellerIssuesOverviewView.name, kwargs={"seller_id": self.seller_1.pk})
        response = self.client.get(url, headers=self.seller_user_1_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["unresolved"], response.data["open"] + response.data["responded"])

    def test_returns_zero_counts_for_seller_without_issues(self):
        url = reverse(SellerIssuesOverviewView.name, kwargs={"seller_id": self.seller_1.pk})
        response = self.client.get(url, headers=self.seller_user_1_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_issues"], 0)
        self.assertEqual(response.data["open"], 0)
        self.assertEqual(response.data["responded"], 0)
        self.assertEqual(response.data["resolved"], 0)
        self.assertEqual(response.data["unresolved"], 0)


class SellerIssueRespondViewTests(IssueReportingAPITestBase):
    def test_post_updates_status_and_seller_response(self):
        issue = self._create_issue(self.posting_1, self.consumer_1, "open", desc="Need reply")
        url = reverse(
            SellerIssueRespondView.name,
            kwargs={"issue_id": issue.issue_id},
        )
        response = self.client.post(
            url,
            {"status": "responded", "seller_response": "Sorry about that."},
            format="json",
            headers=self.seller_user_1_headers
        )

        issue.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(issue.status, "responded")
        self.assertEqual(issue.seller_response, "Sorry about that.")

    def test_post_ignores_non_allowed_fields(self):
        issue = self._create_issue(self.posting_1, self.consumer_1, "open", desc="Original")
        url = reverse(
            SellerIssueRespondView.name,
            kwargs={"issue_id": issue.issue_id},
        )
        response = self.client.post(
            url,
            {"description": "Should not change", "status": "resolved"},
            format="json",
            headers=self.seller_user_1_headers
        )

        issue.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(issue.description, "Original")
        self.assertEqual(issue.status, "resolved")

        issue = self._create_issue(self.posting_3, self.consumer_1, "open")
        url = reverse(
            SellerIssueRespondView.name,
            kwargs={"issue_id": issue.issue_id},
        )
        response = self.client.post(url, {"status": "responded"}, format="json", headers=self.seller_user_1_headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_works_for_non_default_seller_id(self):
        issue = self._create_issue(self.posting_3, self.consumer_1, "open", desc="Need seller two")
        url = reverse(
            SellerIssueRespondView.name,
            kwargs={"issue_id": issue.issue_id},
        )
        response = self.client.post(
            url,
            {"status": "responded", "seller_response": "Acknowledged."},
            format="json",
            headers=self.seller_user_2_headers
        )

        issue.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(issue.status, "responded")
        self.assertEqual(issue.seller_response, "Acknowledged.")