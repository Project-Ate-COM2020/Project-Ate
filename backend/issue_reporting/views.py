from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from core.models import IssueReport
from .serializers import IssueReportSerializer


class SellerIssueRespondView(APIView):
    def patch(self, request, seller_id, issue_id):
        try:
            issue = IssueReport.objects.get(
                issue_id=issue_id,
                posting__seller__seller_id=seller_id,
            )
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
