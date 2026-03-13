from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import BundlePosting, Consumer, IssueReport, Reservation, Seller


class IssueReportingAPITestBase(APITestCase):
	def setUp(self):
		self.seller_1 = Seller.objects.create(
			name="Seller One",
			location="A1",
			password="pw1",
			opening_hours="09:00-17:00",
			contact_stub="s1@example.com",
		)
		self.seller_2 = Seller.objects.create(
			name="Seller Two",
			location="B2",
			password="pw2",
			opening_hours="09:00-17:00",
			contact_stub="s2@example.com",
		)

		self.consumer_1 = Consumer.objects.create(
			display_name="Buyer One",
			password="pw1",
			streak=0,
		)
		self.consumer_2 = Consumer.objects.create(
			display_name="Buyer Two",
			password="pw2",
			streak=0,
		)

		self.posting_1 = self._create_posting(self.seller_1, "Bakery")
		self.posting_2 = self._create_posting(self.seller_1, "Dairy")
		self.posting_3 = self._create_posting(self.seller_2, "Hot Meals")

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
		url = reverse("consumer-create-issue")

		response = self.client.post(
			url,
			{
				"consumer_id": self.consumer_1.consumer_id,
				"posting": self.posting_1.posting_id,
				"type": "Product quality",
				"description": "The bread was stale.",
			},
			format="json",
		)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(IssueReport.objects.count(), 1)
		issue = IssueReport.objects.first()
		self.assertEqual(issue.status, "open")

	def test_create_issue_requires_consumer_and_posting(self):
		url = reverse("consumer-create-issue")
		response = self.client.post(
			url,
			{"type": "Product quality", "description": "Missing ids"},
			format="json",
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_create_issue_rejects_when_bundle_not_collected(self):
		self._create_reservation(self.consumer_1, self.posting_1, "reserved", "C101")
		url = reverse("consumer-create-issue")
		response = self.client.post(
			url,
			{
				"consumer_id": self.consumer_1.consumer_id,
				"posting": self.posting_1.posting_id,
				"type": "Product quality",
				"description": "Should fail",
			},
			format="json",
		)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ConsumerIssuesViewTests(IssueReportingAPITestBase):
	def test_returns_only_selected_consumers_issues(self):
		self._create_issue(self.posting_1, self.consumer_1, desc="Mine")
		self._create_issue(self.posting_2, self.consumer_2, desc="Not mine")

		url = reverse("consumer-issues", kwargs={"consumer_id": self.consumer_1.consumer_id})
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 1)
		self.assertEqual(response.data[0]["description"], "Mine")

	def test_orders_issues_by_created_at_desc(self):
		older = self._create_issue(self.posting_1, self.consumer_1, desc="Older")
		newer = self._create_issue(self.posting_2, self.consumer_1, desc="Newer")
		now = timezone.now()
		IssueReport.objects.filter(issue_id=older.issue_id).update(created_at=now - timedelta(days=2))
		IssueReport.objects.filter(issue_id=newer.issue_id).update(created_at=now - timedelta(days=1))

		url = reverse("consumer-issues", kwargs={"consumer_id": self.consumer_1.consumer_id})
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data[0]["issue_id"], newer.issue_id)
		self.assertEqual(response.data[1]["issue_id"], older.issue_id)

	def test_returns_empty_list_when_consumer_has_no_issues(self):
		url = reverse("consumer-issues", kwargs={"consumer_id": self.consumer_1.consumer_id})
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, [])


class ConsumerReportablePostingsViewTests(IssueReportingAPITestBase):
	def test_returns_only_collected_postings(self):
		self._create_reservation(self.consumer_1, self.posting_1, "collected", "C200")
		self._create_reservation(self.consumer_1, self.posting_2, "reserved", "C201")

		url = reverse(
			"consumer-reportable-postings",
			kwargs={"consumer_id": self.consumer_1.consumer_id},
		)
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 1)
		self.assertEqual(response.data[0]["posting_id"], self.posting_1.posting_id)

	def test_deduplicates_postings_with_multiple_collected_reservations(self):
		self._create_reservation(self.consumer_1, self.posting_1, "collected", "C210")
		self._create_reservation(self.consumer_1, self.posting_1, "collected", "C211")

		url = reverse(
			"consumer-reportable-postings",
			kwargs={"consumer_id": self.consumer_1.consumer_id},
		)
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 1)
		self.assertEqual(response.data[0]["posting_id"], self.posting_1.posting_id)

	def test_returns_empty_when_no_collected_reservations(self):
		self._create_reservation(self.consumer_1, self.posting_1, "reserved", "C220")
		url = reverse(
			"consumer-reportable-postings",
			kwargs={"consumer_id": self.consumer_1.consumer_id},
		)
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, [])


class SellerIssuesViewTests(IssueReportingAPITestBase):
	def test_returns_only_issues_for_given_seller(self):
		own = self._create_issue(self.posting_1, self.consumer_1, desc="Own seller")
		self._create_issue(self.posting_3, self.consumer_1, desc="Other seller")

		url = reverse("seller-issues", kwargs={"seller_id": self.seller_1.seller_id})
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 1)
		self.assertEqual(response.data[0]["issue_id"], own.issue_id)

	def test_orders_seller_issues_by_created_at_desc(self):
		older = self._create_issue(self.posting_1, self.consumer_1, desc="Older")
		newer = self._create_issue(self.posting_2, self.consumer_1, desc="Newer")
		now = timezone.now()
		IssueReport.objects.filter(issue_id=older.issue_id).update(created_at=now - timedelta(days=2))
		IssueReport.objects.filter(issue_id=newer.issue_id).update(created_at=now - timedelta(days=1))

		url = reverse("seller-issues", kwargs={"seller_id": self.seller_1.seller_id})
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data[0]["issue_id"], newer.issue_id)
		self.assertEqual(response.data[1]["issue_id"], older.issue_id)

	def test_returns_empty_when_seller_has_no_issues(self):
		url = reverse("seller-issues", kwargs={"seller_id": self.seller_1.seller_id})
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, [])


class SellerIssuesOverviewViewTests(IssueReportingAPITestBase):
	def test_returns_correct_status_counts(self):
		self._create_issue(self.posting_1, self.consumer_1, "open")
		self._create_issue(self.posting_1, self.consumer_1, "responded")
		self._create_issue(self.posting_2, self.consumer_1, "resolved")

		url = reverse("seller-issues-overview", kwargs={"seller_id": self.seller_1.seller_id})
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["total_issues"], 3)
		self.assertEqual(response.data["open"], 1)
		self.assertEqual(response.data["responded"], 1)
		self.assertEqual(response.data["resolved"], 1)

	def test_unresolved_is_open_plus_responded(self):
		self._create_issue(self.posting_1, self.consumer_1, "open")
		self._create_issue(self.posting_1, self.consumer_1, "responded")
		self._create_issue(self.posting_1, self.consumer_1, "resolved")

		url = reverse("seller-issues-overview", kwargs={"seller_id": self.seller_1.seller_id})
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["unresolved"], response.data["open"] + response.data["responded"])

	def test_returns_zero_counts_for_seller_without_issues(self):
		url = reverse("seller-issues-overview", kwargs={"seller_id": self.seller_1.seller_id})
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["total_issues"], 0)
		self.assertEqual(response.data["open"], 0)
		self.assertEqual(response.data["responded"], 0)
		self.assertEqual(response.data["resolved"], 0)
		self.assertEqual(response.data["unresolved"], 0)


class SellerIssueRespondViewTests(IssueReportingAPITestBase):
	def test_patch_updates_status_and_seller_response(self):
		issue = self._create_issue(self.posting_1, self.consumer_1, "open", desc="Need reply")
		url = reverse(
			"seller-issue-respond",
			kwargs={"seller_id": self.seller_1.seller_id, "issue_id": issue.issue_id},
		)
		response = self.client.patch(
			url,
			{"status": "responded", "seller_response": "Sorry about that."},
			format="json",
		)

		issue.refresh_from_db()
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(issue.status, "responded")
		self.assertEqual(issue.seller_response, "Sorry about that.")

	def test_patch_ignores_non_allowed_fields(self):
		issue = self._create_issue(self.posting_1, self.consumer_1, "open", desc="Original")
		url = reverse(
			"seller-issue-respond",
			kwargs={"seller_id": self.seller_1.seller_id, "issue_id": issue.issue_id},
		)
		response = self.client.patch(
			url,
			{"description": "Should not change", "status": "resolved"},
			format="json",
		)

		issue.refresh_from_db()
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(issue.description, "Original")
		self.assertEqual(issue.status, "resolved")

	def test_patch_returns_404_if_issue_does_not_belong_to_seller(self):
		issue = self._create_issue(self.posting_3, self.consumer_1, "open")
		url = reverse(
			"seller-issue-respond",
			kwargs={"seller_id": self.seller_1.seller_id, "issue_id": issue.issue_id},
		)
		response = self.client.patch(url, {"status": "responded"}, format="json")
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
