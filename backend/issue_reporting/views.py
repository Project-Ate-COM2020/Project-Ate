from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from core.models import BundlePosting, IssueReport, Reservation
from .serializers import IssueReportSerializer


def _seller_issue_queryset(seller_id):
    seller_posting_ids = BundlePosting.objects.filter(
        seller__seller_id=seller_id
    ).values_list("posting_id", flat=True)
    return IssueReport.objects.filter(posting_id__in=seller_posting_ids)


class ConsumerCreateIssueView(APIView):
    def post(self, request):
        consumer_id = request.data.get("consumer_id")
        posting_id = request.data.get("posting")
        issue_type = request.data.get("type")
        description = request.data.get("description")

        if not consumer_id or not posting_id:
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
            status="collected",
        ).exists()

        if not has_reservation:
            return Response(
                {"error": "You can only report bundles you have collected"},
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
    def get(self, request, consumer_id):
        issues = (
            IssueReport.objects
            .filter(consumer__consumer_id=consumer_id)
            .order_by("-created_at")
        )
        serializer = IssueReportSerializer(issues, many=True)
        return Response(serializer.data)


class ConsumerReportablePostingsView(APIView):
    def get(self, request, consumer_id):
        reservations = (
            Reservation.objects
            .select_related("posting")
            .filter(consumer__consumer_id=consumer_id, status="collected")
            .order_by("-posting__created_at")
        )

        seen_postings = set()
        postings = []
        for reservation in reservations:
            posting = reservation.posting
            if posting.posting_id in seen_postings:
                continue
            seen_postings.add(posting.posting_id)
            postings.append({
                "posting_id": posting.posting_id,
                "category": posting.category,
                "pickup_window": posting.pickup_window,
                "seller_id": posting.seller_id,
                "created_at": posting.created_at,
            })

        return Response(postings)


class SellerIssueRespondView(APIView):
    def patch(self, request, seller_id, issue_id):
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
    def get(self, request, seller_id):
        qs = _seller_issue_queryset(seller_id)
        counts = qs.aggregate(
            total=Count("issue_id"),
            open=Count("issue_id", filter=Q(status="open")),
            responded=Count("issue_id", filter=Q(status="responded")),
            resolved=Count("issue_id", filter=Q(status="resolved")),
        )
        return Response({
            "total_issues": counts["total"],
            "open": counts["open"],
            "responded": counts["responded"],
            "resolved": counts["resolved"],
            "unresolved": counts["open"] + counts["responded"],
        })


class SellerIssuesView(APIView):
    def get(self, request, seller_id):
        issues = (
            _seller_issue_queryset(seller_id)
            .order_by("-created_at")
        )
        serializer = IssueReportSerializer(issues, many=True)
        return Response(serializer.data)
