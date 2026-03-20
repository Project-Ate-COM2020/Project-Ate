from django.conf import settings
from django.db import models
from django.db.models import OneToOneField


class Consumer(models.Model):
    consumer_id = models.AutoField(primary_key=True)
    user = OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="consumer"
    )
    display_name = models.CharField(max_length=255)
    streak = models.IntegerField(default=0)
    co2_saved = models.IntegerField(default=0)
    categories_collected = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "consumer"
