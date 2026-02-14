from django.db import models


class Seller(models.Model):
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=6)
    password = models.CharField(max_length=150)
    opening_hours = models.CharField(max_length=20)
    contact_stub = models.CharField(max_length=20)


class Bundle(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    category = models.CharField(max_length=20)
    contents = models.TextField()
    allergens = models.TextField()
    quantity = models.IntegerField()
    price = models.FloatField()
    pickup_window = models.CharField(max_length=20)
    status = models.IntegerField()


class Consumer(models.Model):
    display_name = models.CharField(max_length=20)
    password = models.CharField(max_length=150)
    streak = models.IntegerField()
    badges = models.TextField()


class BundlePosting(models.Model):
    posting_id = models.AutoField(primary_key=True)

    category = models.CharField(max_length=100)
    contents = models.TextField()
    allergens = models.TextField(null=True, blank=True)

    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pickup_window = models.CharField(max_length=50)

    status = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    seller_id = models.IntegerField()

    class Meta:
        db_table = "bundle_posting"
        managed = False

    def __str__(self):
        return f"BundlePosting({self.posting_id})"


class Reservation(models.Model):
    posting = models.ForeignKey(
        BundlePosting,
        db_column="posting_id",     # ✅ IMPORTANT: maps to posting_id in DB
        on_delete=models.CASCADE,
        related_name="reservations",
    )
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    claim_code = models.CharField(max_length=20)
    status = models.IntegerField()

         

      