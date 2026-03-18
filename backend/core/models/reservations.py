from django.db import models

from core.models.bundles import BundlePosting
from core.models.consumer import Consumer


class Reservation(models.Model):
    STATUS_CHOICES = [
        ("reserved", "Reserved"),
        ("collected", "Collected"),
        ("no-show", "No-show"),
        ("expired", "Expired"),
    ]

    reservation_id = models.AutoField(primary_key=True)
    posting = models.ForeignKey(
        BundlePosting, on_delete=models.CASCADE, related_name="reservations"
    )
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    claim_code = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    no_show_reason = models.TextField(null=True, blank=True)
    collected_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "reservation"
