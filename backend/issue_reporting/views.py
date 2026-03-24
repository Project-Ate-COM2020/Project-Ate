from django.template.context_processors import request
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q

from authentication.permissions import IsConsumer, IsSeller, IsConsumerOrSeller
from core.models import BundlePosting, IssueReport, Reservation, Consumer, Seller
from .serializers import IssueReportSerializer


REPORTABLE_RESERVATION_STATUSES = ["reserved", "active", "collected"]


def _seller_issue_queryset(seller_id):
    seller_posting_ids = BundlePosting.objects.filter(
        seller_id=seller_id
    ).values_list("posting_id", flat=True)
    return IssueReport.objects.filter(posting_id__in=seller_posting_ids)


class ConsumerCreateIssueView(APIView):
    name = "consumer-create-issue"
    permission_classes = [IsConsumer]

    def post(self, request):
        user = request.user
        consumer = Consumer.objects.get(user=user)

        consumer_id = consumer.pk
        posting_id = request.data.get("posting")
        issue_type = request.data.get("type")
        description = request.data.get("description")

        if not posting_id:
            return Response(
                {"error": "consumer_id and posting are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not issue_type or not description:
            return Response(
                {"error": "type and description are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        has_reservation = Reservation.objects.filter(
            consumer__consumer_id=consumer_id,
            posting__posting_id=posting_id,
            status__in=REPORTABLE_RESERVATION_STATUSES,
        ).exists()

        if not has_reservation:
            return Response(
                {"error": "You can only report bundles you have reserved or collected"},
                status=status.HTTP_403_FORBIDDEN,
            )

        data = {
            "posting": posting_id,
            "consumer": consumer_id,
            "type": issue_type,
            "description": description,
            "status": "open",
        }
        serializer = IssueReportSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConsumerIssuesView(APIView):
    name = "consumer-issues"
    permission_classes = [IsConsumer]

    def get(self, request):
        consumer_id = request.user.consumer.pk
        issues = (
            IssueReport.objects
            .filter(consumer__consumer_id=consumer_id)
            .order_by("-created_at")
        )
        serializer = IssueReportSerializer(issues, many=True)
        return Response(serializer.data)


class ConsumerReportablePostingsView(APIView):
    name = "consumer-reportable-postings"
    permission_classes = [IsConsumer]

    def get(self, request):
        user = request.user
        consumer = Consumer.objects.get(user=user)
        consumer_id = consumer.pk
        reservations = (
            Reservation.objects
            .select_related("posting")
            .filter(
                consumer__consumer_id=consumer_id,
                status__in=REPORTABLE_RESERVATION_STATUSES,
            )
            .order_by("-timestamp")
        )

        postings = []
        for reservation in reservations:
            posting = reservation.posting
            postings.append({
                "reservation_id": reservation.reservation_id,
                "posting_id": posting.posting_id,
                "category": posting.category,
                "pickup_window": posting.pickup_window,
                "status": reservation.status,
                "ordered_at": reservation.timestamp,
                "seller_id": posting.seller_id,
                "created_at": posting.created_at,
            })

        return Response(postings)


class SellerIssueRespondView(APIView):
    name = "seller-issue-response"
    permission_classes = [IsSeller]

    def post(self, request, issue_id):
        user = request.user
        seller = Seller.objects.get(user=user)
        seller_id = seller.pk
        try:
            issue = _seller_issue_queryset(seller_id).get(issue_id=issue_id)
        except IssueReport.DoesNotExist:
            return Response(
                {"error": "Issue not found for this seller"},
                status=status.HTTP_404_NOT_FOUND,
            )

        allowed_fields = {"seller_response", "status"}
        data = {k: v for k, v in request.data.items() if k in allowed_fields}

        serializer = IssueReportSerializer(issue, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SellerIssuesOverviewView(APIView):
    name = "seller-issues-overview"
    permission_classes = [IsConsumerOrSeller]

    def get(self, request, seller_id):
        is_seller = IsSeller().has_permission(request, self)

        if is_seller and seller_id != request.user.seller.pk:
            return Response(HTTP_403_FORBIDDEN)

        qs = _seller_issue_queryset(seller_id)
        counts = qs.aggregate(
            open=Count("issue_id", filter=Q(status="open")),
            responded=Count("issue_id", filter=Q(status="responded")),
            resolved=Count("issue_id", filter=Q(status="resolved")),
        )
        return Response({
            "total_issues": qs.count(),
            "open": counts["open"],
            "responded": counts["responded"],
            "resolved": counts["resolved"],
            "unresolved": counts["open"] + counts["responded"],
        })


class SellerIssuesView(APIView):
    name = "seller-issues"
    permission_classes = [IsSeller]

    def get(self, request):
        issues = (
            _seller_issue_queryset(request.user.seller.pk)
            .order_by("-created_at")
        )
        serializer = IssueReportSerializer(issues, many=True)
        return Response(serializer.data)