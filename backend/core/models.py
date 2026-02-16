from django.db import models

# Create your models here.

# I MADE THE DATABASES IN DBEAVER, I WILL PASTE THE RAW SQL HERE FOR REFERENCE

# Forecast Input Table
"""CREATE TABLE forecast_input (
  record_id INTEGER PRIMARY KEY AUTOINCREMENT,
  day_of_week INTEGER NOT NULL CHECK (day_of_week BETWEEN 1 AND 7),
  time_window TEXT NOT NULL,
  seller_id INTEGER,
  category TEXT,
  price REAL,
  weather_flag INTEGER NOT NULL DEFAULT 0 CHECK (weather_flag IN (0,1)),
  observed_reservations INTEGER NOT NULL CHECK (observed_reservations >= 0),
  observed_no_show INTEGER NOT NULL CHECK (observed_no_show >= 0),
  FOREIGN KEY (seller_id) REFERENCES seller(seller_id)
);"""


#-- reservation definition

"""CREATE TABLE reservation (
  reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
  posting_id INTEGER NOT NULL,
  consumer_id INTEGER NOT NULL,
  timestamp TEXT NOT NULL DEFAULT (datetime('now')),
  claim_code TEXT NOT NULL UNIQUE,
  status TEXT NOT NULL CHECK (status IN ('reserved','collected','no-show','expired')),
  no_show_reason TEXT,
  collected_at TEXT,
  FOREIGN KEY (posting_id) REFERENCES bundle_posting(posting_id),
  FOREIGN KEY (consumer_id) REFERENCES consumer(consumer_id)
);"""

#-- consumer definition

"""CREATE TABLE consumer (
  consumer_id INTEGER PRIMARY KEY AUTOINCREMENT,
  display_name TEXT NOT NULL,
  streak INTEGER NOT NULL DEFAULT 0,
  badges TEXT
);"""

#-- seller definition

"""CREATE TABLE seller (
  seller_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  location TEXT NOT NULL,
  opening_hours TEXT,
  contact_stub TEXT
);"""

#-- issue_report definition

"""CREATE TABLE issue_report (
  issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
  posting_id INTEGER NOT NULL,
  consumer_id INTEGER,
  type TEXT NOT NULL,
  description TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('open','responded','resolved')),
  seller_response TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (posting_id) REFERENCES bundle_posting(posting_id),
  FOREIGN KEY (consumer_id) REFERENCES consumer(consumer_id)
);"""

#-- bundle_posting definition

"""CREATE TABLE bundle_posting (
  posting_id INTEGER PRIMARY KEY AUTOINCREMENT,
  seller_id INTEGER NOT NULL,
  category TEXT NOT NULL,
  contents TEXT,
  allergens TEXT,
  quantity INTEGER NOT NULL CHECK (quantity >= 0),
  quantity_remaining INTEGER NOT NULL CHECK (quantity_remaining >= 0),
  price REAL NOT NULL CHECK (price >= 0),
  pickup_window TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('active','expired','completed','cancelled')),
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (seller_id) REFERENCES seller(seller_id)
);"""

#-- forecast_output definition

"""CREATE TABLE forecast_output (
  output_id INTEGER PRIMARY KEY AUTOINCREMENT,
  posting_id INTEGER,
  predicted_reservations REAL NOT NULL CHECK (predicted_reservations >= 0),
  predicted_no_show_prob REAL NOT NULL CHECK (predicted_no_show_prob BETWEEN 0 AND 1),
  confidence TEXT,
  rationale TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (posting_id) REFERENCES bundle_posting(posting_id)
);"""

class Seller(models.Model):
    seller_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    opening_hours = models.TextField(null=True, blank=True)
    contact_stub = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'seller'

class Consumer(models.Model):
    consumer_id = models.AutoField(primary_key=True)
    display_name = models.CharField(max_length=255)
    streak = models.IntegerField(default=0)
    badges = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'consumer'

class BundlePosting(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    posting_id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)
    contents = models.TextField(null=True, blank=True)
    allergens = models.TextField(null=True, blank=True)
    quantity = models.IntegerField()
    quantity_remaining = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pickup_window = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bundle_posting'

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('reserved', 'Reserved'),
        ('collected', 'Collected'),
        ('no-show', 'No-show'),
        ('expired', 'Expired'),
    ]
    
    reservation_id = models.AutoField(primary_key=True)
    posting = models.ForeignKey(BundlePosting, on_delete=models.CASCADE)
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    claim_code = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    no_show_reason = models.TextField(null=True, blank=True)
    collected_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'reservation'

class IssueReport(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('responded', 'Responded'),
        ('resolved', 'Resolved'),
    ]
    
    issue_id = models.AutoField(primary_key=True)
    posting = models.ForeignKey(BundlePosting, on_delete=models.CASCADE)
    consumer = models.ForeignKey(Consumer, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    seller_response = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'issue_report'

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
        db_table = 'forecast_input'

class ForecastOutput(models.Model):
    output_id = models.AutoField(primary_key=True)
    posting = models.ForeignKey(BundlePosting, on_delete=models.CASCADE, null=True, blank=True)
    predicted_reservations = models.DecimalField(max_digits=10, decimal_places=2)
    predicted_no_show_prob = models.DecimalField(max_digits=3, decimal_places=2)
    confidence = models.CharField(max_length=255, null=True, blank=True)
    rationale = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'forecast_output'