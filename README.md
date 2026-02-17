Exeter University  
Module COM2020 (Team Project)  
Project 8  
Tech stack: React + Django + SQLite  
In essence this is a web app allows a user to send a request  
that request either updates data in the db, or returns data from the db to the user  

# Project-Ate

A Django + React web application for connecting food sellers with consumers to reduce food waste.

## Features

- **Seller Dashboard**: Manage listings, track reservations, and view analytics
   - **Forecasting**: model based demand prediction for optimal pricing
   - **Analytics**: Track revenue, food waste reduction, and no-show rates
   - **Bundle Management**: Mark reservations as collected, Create new bundles to sell

- **Consumer Portal**: Browse available food bundles and make reservations

- **Consumer Orders Page**: View reservations, expiry times and claim codes

- **Consumer Game Page**: View current streaks, statistics and CO2 saved


## Project Structure
Project-Ate/
├── backend/ # Django REST API
├── frontend/ # React app (if applicable)
└── docs/ # Documentation


## Setup Instructions

### Backend

1. Navigate to the backend folder:
```bash
cd backend
```

2. Instal dependancies
```bash
pip install -r requirements.txt
```

3. Run migrations  and start development server
``` bash
python manage.py migrate
```

4. Start development server
``` bash
python manage.py runserver
```

The server runs at http://127.0.0.1:8000/

### Frontend

1. Navigate to frontend folder
``` bash
cd frontend
```

2. Install dependancies
npm install

3. Start development server
npm start

### Run tests
python manage.py test seller.tests
python manage.py test forecasts.tests
python manage.py test analytics.tests

API ENDPOINTS
Seller (/seller/)
GET /seller/getsellername/ - Get seller name
GET /seller/getselleraddress/ - Get seller address
GET /seller/getreservations/ - Get seller reservations
POST /seller/createlisting/ - Create a new listing

Marketplace (/marketplace/)
Global Bundle Operations
POST /marketplace/bundle/ - Create bundle
GET /marketplace/bundles/ - Get all bundles
GET /marketplace/bundles/between?from=X&to=Y&exclusive=false - Get bundles between dates
GET /marketplace/bundles/oldest?count=20 - Get oldest bundles
GET /marketplace/bundles/older/?date=YYYY-MM-DD - Get bundles older than date
GET /marketplace/bundles/newer/?date=YYYY-MM-DD - Get bundles newer than date
GET /marketplace/bundles/open/ - Get bundles from open shops
GET /marketplace/bundles/open?from=YYYY-MM-DDTHH:MM:SS±HH:MM&to=... - Get open bundles in time range
GET /marketplace/bundles/collection/?from=YYYY-MM-DDTHH:MM:SS±HH:MM&to=... - Get bundles with collection in range
GET /marketplace/bundle/<bundle_id>/ - Get specific bundle

Consumer
POST /marketplace/consumer - Create consumer
GET /marketplace/consumer/<consumer_id>/ - Get consumer data

Seller Operations
POST /marketplace/seller - Create seller
GET /marketplace/seller/<seller_id>/ - Get seller data
GET /marketplace/seller/<seller_id>/bundles - Get seller's bundles
GET /marketplace/seller/<seller_id>/bundles/between - Get seller bundles between dates
GET /marketplace/seller/<seller_id>/bundles/newest - Get seller's newest bundles
GET /marketplace/seller/<seller_id>/bundles/oldest - Get seller's oldest bundles
GET /marketplace/seller/<seller_id>/bundles/older/ - Get seller bundles older than date
GET /marketplace/seller/<seller_id>/bundles/younger/ - Get seller bundles younger than date
GET /marketplace/seller/<seller_id>/bundles/collection/ - Get seller bundles with collection in range

Reservations
POST /marketplace/reservations - Create reservation
GET /marketplace/reservations/<reservation_id>/ - Get reservation data

Authentication
POST /marketplace/seller/auth/token - Seller login
POST /marketplace/seller/auth/token/refresh - Refresh seller token
POST /marketplace/seller/auth/token/verify/ - Verify seller token
POST /marketplace/consumer/auth/token - Consumer login
POST /marketplace/consumer/auth/token/refresh - Refresh consumer token
POST /marketplace/consumer/auth/token/verify/ - Verify consumer token

Analytics (/analytics/)
GET /analytics/total-listings/ - Get total listings count
GET /analytics/total-revenue/ - Get total revenue
GET /analytics/total-reservations/ - Get total reservations
GET /analytics/food-waste-reduction/ - Get food waste reduction %
GET /analytics/total-no-shows/ - Get total no-shows

Game (/game/)
GET /game/api/game/summary/ - Get game summary
GET /game/api/game/recent/ - Get recent rescues
GET /game/api/test/ - Test endpoint

Technologies
Backend: Django, Django REST Framework, djangorestframework-simplejwt
Frontend: React (if applicable)
Database: SQLite (dev) / PostgreSQL (prod)
AI/ML: Forecasting algorithms for demand prediction
Contributing
Create a feature branch
Commit changes
Push and create a pull request
