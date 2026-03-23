from rest_framework import serializers
from core.models import IssueReport, Consumer, BundlePosting


class ConsumerNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumer
        fields = ["consumer_id", "display_name"]


class BundlePostingNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = BundlePosting
        fields = ["posting_id", "category"]


class IssueReportSerializer(serializers.ModelSerializer):
    consumer = ConsumerNestedSerializer(allow_null=True)
    posting = BundlePostingNestedSerializer()

    class Meta:
        model = IssueReport
        fields = "__all__"