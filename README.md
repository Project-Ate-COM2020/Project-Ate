# Project-Ate

A Django + React web application for connecting food sellers with consumers to help solve the food waste problem.

Members: James Clarke, Jacob Evans, Harry Price, Will Brown, Anna Hedley, Lucas Parish, Zac Dowlands

This GitHub Repo is strictly for code, for documentation please see our submission

## Features

- **Seller Dashboard**: Manage listings, track reservations, and view analytics
   - **Forecasting**: model based demand prediction for optimal pricing
   - **Analytics**: Track revenue, food waste reduction, and no-show rates
   - **Bundle Management**: Mark reservations as collected, Create new bundles to sell

- **Consumer Portal**: Browse available food bundles and make reservations

- **Consumer Orders Page**: View reservations, expiry times and claim codes

- **Consumer Game Page**: View current streaks, statistics and CO2 saved


## Project Structure

```
Project-Ate/
	backend/
		manage.py                     # Django server manager
		requirements.txt              # Python dependencies
		db.sqlite3                    # SQLite database
		backend/
			__init__.py
			settings.py               # Server settings and installed apps
			urls.py                   # Root URL routing
			asgi.py
			wsgi.py                   # WSGI config for deployment
		core/
			__init__.py
			models.py                 # Core database models
			admin.py
			apps.py
			tests.py
			urls.py
			migrations/
		marketplace/
			__init__.py
			models.py
			admin.py
			apps.py
			urls.py                   # Marketplace API endpoints
			serializers.py            # JSON serialization
			consumer_token.py
			seller_token.py
			tests.py
			views/
				__init__.py
				bundles.py
			migrations/
		seller/
			__init__.py
			admin.py
			apps.py
			serializers.py
			views.py
			urls.py
			tests.py
			migrations/
		buyer/
			__init__.py
			admin.py
			apps.py
			models.py
			serializers.py
			views.py
			urls.py
			migrations/
		analytics/
			__init__.py
			admin.py
			apps.py
			models.py
			serializers.py
			views.py
			urls.py
			analytics.py              # Analytics business logic
			tests.py
			migrations/
		forecasts/
			__init__.py
			admin.py
			apps.py
			serializers.py
			views.py
			urls.py
			forecasting.py            # Forecasting algorithms
			tests.py
			migrations/
		game/
			__init__.py
			admin.py
			apps.py
			models.py
			serializers.py
			views.py
			urls.py
			game.py                   # Game logic
			tests.py
			migrations/
	
   frontend/                       # Slightly less well documented the frontend is, this is a general directory structure, there's a lot of cleaning up that needs to be done
		src/
			App.jsx
			main.jsx
			api/
			assets/
			authorisationPages/
			Basket/
			gamePages/
			homePage/
			marketplacePages/
			orders/
			reusableComponents/
			seller/
		public/
		package.json
		vite.config.js
		index.html
	DevOps/
	Environment Documentation/
	Project Documentation/
```


## Depolyment Guide

### Backend

1. Navigate to the backend folder:
```bash
cd backend
```

2. Instal dependancies
```bash
pip install -r requirements.txt
```

3. Run migrations and start development server
``` bash
python manage.py migrate
python manage.py runserver
```

The backend server runs at http://127.0.0.1:8000/

### Frontend

1. Navigate to frontend folder
``` bash
cd frontend
```

2. Install dependancies
``` bash
npm install
```

3. Start development server
``` bash
npm run dev
```

The frontend runs at http://127.0.0.1:5173/

### Run tests

To run our testing suite:
``` bash
python manage.py test seller.tests
python manage.py test forecasts.tests
python manage.py test analytics.tests
```

## API Endpoints

### Seller Endpoints (mostly for demo only, will be encompassed by marketplace in sprint 2)
(/seller/)

```
GET /seller/getsellername/ - Get seller name
GET /seller/getselleraddress/ - Get seller address
GET /seller/getreservations/ - Get seller reservations
POST /seller/createlisting/ - Create a new listing
```

### Marketplace 
(/marketplace/)

#### Global Bundle Operations
```
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
```

#### Consumer Operations
```
POST /marketplace/consumer - Create consumer
GET /marketplace/consumer/<consumer_id>/ - Get consumer data
```

#### Seller Operations
```
POST /marketplace/seller - Create seller
GET /marketplace/seller/<seller_id>/ - Get seller data
GET /marketplace/seller/<seller_id>/bundles - Get seller's bundles
GET /marketplace/seller/<seller_id>/bundles/between - Get seller bundles between dates
GET /marketplace/seller/<seller_id>/bundles/newest - Get seller's newest bundles
GET /marketplace/seller/<seller_id>/bundles/oldest - Get seller's oldest bundles
GET /marketplace/seller/<seller_id>/bundles/older/ - Get seller bundles older than date
GET /marketplace/seller/<seller_id>/bundles/younger/ - Get seller bundles younger than date
GET /marketplace/seller/<seller_id>/bundles/collection/ - Get seller bundles with collection in range
```

#### Reservations
```
POST /marketplace/reservations - Create reservation
GET /marketplace/reservations/<reservation_id>/ - Get reservation data
```

#### Authentication
```
POST /marketplace/seller/auth/token - Seller login
POST /marketplace/seller/auth/token/refresh - Refresh seller token
POST /marketplace/seller/auth/token/verify/ - Verify seller token
POST /marketplace/consumer/auth/token - Consumer login
POST /marketplace/consumer/auth/token/refresh - Refresh consumer token
POST /marketplace/consumer/auth/token/verify/ - Verify consumer token
```

### Analytics 
(/analytics/)

```
GET /analytics/total-listings/ - Get total listings count
GET /analytics/total-revenue/ - Get total revenue
GET /analytics/total-reservations/ - Get total reservations
GET /analytics/food-waste-reduction/ - Get food waste reduction %
GET /analytics/total-no-shows/ - Get total no-shows
```

### Game 
(/game/)

```
GET /game/api/game/summary/ - Get game summary
GET /game/api/game/recent/ - Get recent rescues
GET /game/api/test/ - Test endpoint
```

## Frontend Pages

### Seller
```
/seller - Seller dashboard, contains analytics, bundles and forecasting
```

### Consumer
```
/user - User homepage, contains bundles available to reserve
/orders - contains current reservations for the consumer
/game - shows CO2 saved, streaks and other stats
```

### Authentication
```
/login - allows a user who has an account to sign in
/signup/seller - allows a user to create a seller account
/signup/user - allows a user to create a consumer account
```

