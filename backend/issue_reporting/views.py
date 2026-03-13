from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from core.models import IssueReport
from .serializers import IssueReportSerializer


class SellerIssuesOverviewView(APIView):
    def get(self, request, seller_id):
        qs = IssueReport.objects.filter(posting__seller__seller_id=seller_id)
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
            IssueReport.objects
            .filter(posting__seller__seller_id=seller_id)
            .order_by("-created_at")
        )
        serializer = IssueReportSerializer(issues, many=True)
        return Response(serializer.data)
