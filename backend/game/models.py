from django.db import models

# Create your models here.

##defining the consumer table to django
class Consumer(models.Model):
    consumer_id = models.AutoField(primary_key=True)
    display_name = models.CharField(max_length=50)
    streak = models.IntegerField(default=0)
    badges = models.JSONField(default=list)
    ##making badges a list so names of the badges can be put in there

##defining the reservation table to django
class Reservation(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    posting_id = models.IntegerField()
    ##keeping posting_id as just a number for now, can be changed to a foreign key later
    consumer_id = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    ##establishing consumer_id as a foreign key so we can do the recent reservations count
    ##if a consumer is deleted then reservations are also deleted 
    STATUS_CHOICES = [("no-show", "No show"), ("collected", "Collected"), ("expired", "Expired")]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    ##defines status as only being able to take the values no-show, collected or expired
    collected_at = models.DateTimeField() 

    