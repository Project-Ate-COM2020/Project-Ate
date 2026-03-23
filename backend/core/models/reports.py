from django.contrib.auth import get_user_model
from django.db import models

from core.models.bundles import BundlePosting
from core.models.consumer import Consumer
from core.models.seller import Seller


# if a consumer is reported
class ConsumerReport(models.Model):
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "consumer_report"


# if a seller is reported
class SellerReport(models.Model):
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "seller_report"


class IssueReport(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("responded", "Responded"),
        ("resolved", "Resolved"),
    ]

    issue_id = models.AutoField(primary_key=True)
    posting = models.ForeignKey(BundlePosting, on_delete=models.CASCADE)
    consumer = models.ForeignKey(
        Consumer, on_delete=models.SET_NULL, null=True, blank=True
    )
    type = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    seller_response = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "issue_report"
