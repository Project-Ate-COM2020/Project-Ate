from rest_framework import serializers
from core.models import IssueReport


class IssueReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueReport
        fields = "__all__"