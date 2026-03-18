from django.db import models

from core.models.bundles import BundlePosting
from core.models.seller import Seller


class ForecastInput(models.Model):
    record_id = models.AutoField(primary_key=True)
    day_of_week = models.IntegerField()
    time_window = models.CharField(max_length=255)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    weather_flag = models.IntegerField(default=0)
    observed_reservations = models.IntegerField()
    observed_no_show = models.IntegerField()
    unreserved_stock = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "forecast_input"


class ForecastOutput(models.Model):
    output_id = models.AutoField(primary_key=True)
    posting = models.ForeignKey(
        BundlePosting, on_delete=models.CASCADE, null=True, blank=True
    )
    predicted_reservations = models.DecimalField(max_digits=10, decimal_places=2)
    predicted_no_show_prob = models.DecimalField(max_digits=3, decimal_places=2)
    confidence = models.CharField(max_length=255, null=True, blank=True)
    rationale = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "forecast_output"
