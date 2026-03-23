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
    class Meta:
        model = IssueReport
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["consumer"] = (
            ConsumerNestedSerializer(instance.consumer).data
            if instance.consumer is not None
            else None
        )
        data["posting"] = (
            BundlePostingNestedSerializer(instance.posting).data
            if instance.posting is not None
            else None
        )
        return data