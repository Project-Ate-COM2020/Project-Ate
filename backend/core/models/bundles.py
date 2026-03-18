from django.db import models
from django.db.models import CheckConstraint, Q

from core.models.seller import Seller


class BundlePosting(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("expired", "Expired"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    posting_id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="bundles")
    category = models.CharField(max_length=255)
    contents = models.TextField(null=True, blank=True)
    quantity = models.IntegerField()
    quantity_remaining = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pickup_window = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "bundle_posting"

        constraints = [
            CheckConstraint(
                name="quantity_remaining_less_than_quantity",
                check=Q(quantity_remaining__lt=models.F("quantity")),
            )
        ]


class Allergen(models.Model):
    allergen_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "allergens"


class BundleAllergens(models.Model):
    bundle_id = models.ForeignKey(BundlePosting, on_delete=models.CASCADE)
    allergen_id = models.ForeignKey(Allergen, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("bundle_id", "allergen_id")
