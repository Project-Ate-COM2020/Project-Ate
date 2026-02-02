from django.db import models

# Create your models here.

# defining the consumer table to django
class Consumer(models.Model):
    consumer_id = models.AutoField(primary_key=True)
    display_name = models.CharField(max_length=50)
    streak = models.IntegerField(default=0)
    badges = models.JSONField(default=list)
    # making badges a list so names of the badges can be put in there

# defining the reservation table to django
class Reservation(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    posting_id = models.IntegerField()
    # keeping posting_id as just a number for now, can be changed to a foreign key later
    consumer_id = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    # establishing consumer_id as a foreign key so we can do the recent reservations count
    # if a consumer is deleted then reservations are also deleted 
    timestamp = models.DateTimeField()
    claim_code = models.CharField(max_length=20)
    STATUS_CHOICES = [("no-show", "No show"), ("collected", "Collected"), ("expired", "Expired")]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    # defines status as only being able to take the values no-show, collected or expired
    no_show_reason = models.CharField(max_length=50)
    collected_at = models.DateTimeField() 

# defining the bundle_posting table to django
class Bundle_Posting(models.Model):
    posting_id = models.AutoField(primary_key=True)
    seller_id = models.IntegerField()
    # keeping seller_id as just a number as it does not need to be used
    CATEGORY_CHOICES = [
        ("Hot Meals", "hot meals"),
        ("Fresh Produce", "fresh produce"),
        ("Prepared Salads", "prepared salads"),
        ("Bakery", "bakery"),
        ("Desserts", "desserts"),
        ("Dairy", "dairy")
    ]
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    # defines category as only being able to take the values of the six types of food
    contents = models.CharField(max_length=50)
    allergens = models.CharField(max_length=50)
    quantity = models.IntegerField()
    quantity_remaining = models.IntegerField()
    price = models.FloatField()
    pickup_window = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField() 