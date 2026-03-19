from django.db import models

from core.models.consumer import Consumer


class Badges(models.Model):
    badge_id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=30)
    description = models.TextField()
    earned_at = models.DateTimeField()

    class Meta:
        db_table = "badges"


class BadgeMapping(models.Model):
    badge_id = models.ForeignKey(Badges, on_delete=models.CASCADE)
    consumer_id = models.ForeignKey(Consumer, on_delete=models.DO_NOTHING, related_name="badges")

    class Meta:
        unique_together = ("badge_id", "consumer_id")
