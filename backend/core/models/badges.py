from django.db import models

from core.models.consumer import Consumer


class Badges(models.Model):
    badge_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=30)
    description = models.TextField(null=True)
    min_categories = models.IntegerField()
    min_co2 = models.IntegerField()

    class Meta:
        db_table = "badges"


class BadgeMapping(models.Model):
    badge_id = models.ForeignKey(
        Badges, on_delete=models.CASCADE, related_name="consumers_who_have_earned"
    )
    consumer_id = models.ForeignKey(
        Consumer, on_delete=models.DO_NOTHING, related_name="badges"
    )
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("badge_id", "consumer_id")
