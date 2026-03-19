from django.db import models

from core.models.consumer import Consumer
from core.models.seller import Seller


class SellerReview(models.Model):
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    stars = models.IntegerField()
    title = models.CharField(max_length=50)
    review = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "seller_review"


class ConsumerReview(models.Model):
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    stars = models.IntegerField()
    title = models.CharField(max_length=50)
    review = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "consumer_review"
