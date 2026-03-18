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

# -- reservation definition

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

# -- consumer definition

"""CREATE TABLE consumer (
  consumer_id INTEGER PRIMARY KEY AUTOINCREMENT,
  display_name TEXT NOT NULL,
  streak INTEGER NOT NULL DEFAULT 0,
  badges TEXT
);"""

# -- seller definition

"""CREATE TABLE seller (
  seller_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  location TEXT NOT NULL,
  opening_hours TEXT,
  contact_stub TEXT
);"""

# -- issue_report definition

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

# -- bundle_posting definition

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

# -- forecast_output definition

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

from .badges import *
from .bundles import *
from .reservations import *
from .consumer import *
from .user import *
from .seller import *
from .reports import *
from .reviews import *
from .forecasting import *
from .maintainer import *
