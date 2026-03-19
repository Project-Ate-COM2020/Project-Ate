# Project-Ate

Project-Ate is a full-stack web application built to reduce food waste by connecting food sellers with consumers who can reserve surplus food bundles at reduced prices.

## Overview

The platform provides:

- A **seller workflow** for listing bundles, managing reservations, and tracking outcomes
- A **consumer workflow** for browsing bundles, reserving food, and tracking rescue impact
- **Analytics and forecasting** capabilities to support stock decisions and waste reduction
- A **gamified consumer view** for engagement through rescue statistics and streaks

## Tech Stack

- **Backend:** Django 5, Django REST Framework, SimpleJWT
- **Frontend:** React 19, Vite (development), React Router, Axios
- **Database:** SQLite (development)

## Repository Structure

```text
Project-Ate/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── backend/               # Django project configuration
│   ├── marketplace/           # Bundle, seller, consumer, reservation APIs
│   ├── seller/                # Seller-specific APIs
│   ├── buyer/                 # Buyer-related logic
│   ├── forecasts/             # Forecasting endpoints and logic
│   ├── analytics/             # Analytics endpoints and calculations
│   ├── game/                  # Gamification endpoints
│   ├── issue_reporting/       # Issue reporting domain
│   └── core/                  # Shared/core models
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   └── src/                   # Current factoring to change drastically
│       ├── authorisationPages/ 
│       ├── marketplacePages/
│       ├── seller/
│       ├── orders/
│       ├── gamePages/
│       └── reusableComponents/
└── Environment Documentation/
```

## Quick Start

### Prerequisites

- Python 3.11+ (recommended)
- Node.js 20+ and npm
- `pip`

### 1) Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Backend runs on `http://127.0.0.1:8000/`.

### 2) Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://127.0.0.1:5173/`.

## Configuration Notes

- Current backend settings are configured for local development.
- CORS currently allows `localhost:5173` and `127.0.0.1:5173`.
- JWT authentication is enabled for protected APIs.
- Do **not** use the current development settings as-is for production deployment.

## Running Tests

From `backend/`:

```bash
python manage.py test seller.tests
python manage.py test forecasts.tests
python manage.py test analytics.tests
python manage.py test marketplace.tests
python manage.py test authentication.tests
```

## API Overview

Base URL: `http://127.0.0.1:8000/`

### Authentication (`/authentication`)

- `POST /auth/user` create a base user
- `POST /auth/token` retrieve a JWT for the account with username and password
- `POST /auth/refresh` refresh a JWT using the users refresh JWT
- `POST /auth/verify` verify whether a token is valid
- `GET /auth/test/seller` returns ok if request is made by seller
- `GET /auth/test/consumer` returns ok if request is made by consumer
- `GET /auth/test/maintainer` returned ok if request is made by maintainer
- `GET /auth/test/consumer-or-seller` returns ok if request is made by consumer or seller
- `GET /auth/test/consumer-and-seller` returns ok if request is made by consumer and seller
- `GET /auth/test/maintainer-or-seller` returns ok if request is made by maintainer or seller
- `GET /auth/test/maintainer-and-seller` returns ok if request is made by maintainer and seller
- `GET /auth/test/maintainer-or-consumer` returns ok if request is made by maintainer or consumer
- `GET /auth/test/maintainer-and-consumer` returns ok if request is made by maintainer and consumer
- `GET /auth/test/maintainer-or-consumer-or-seller` returns ok if request is made by maintainer or consumer or seller
- `GET /auth/test/maintainer-and-consumer-and-seller `returns ok if request is made by maintainer and consumer and seller

### Marketplace (`/marketplace/`)

- Bundles: create and retrieve bundle listings
- Sellers/Consumers: create and retrieve profile entities
- Reservations: create and fetch reservation records
- Auth: seller and consumer JWT issue/refresh/verify

Representative endpoints:

- `POST /marketplace/bundle/` create a marketplace bundle
- `GET /marketplace/bundle/list` retrieve a list of bundles by page
- `GET or PUT or PATCH or Delete /marketplace/bundle/<bundle_id>/` retrieve, update or delete bundle by primary key
- `POST /marketplace/reservations`

### Forecasting (`/forecast/`)

Representative endpoint:

- `GET /forecast/prediction/`

### Analytics (`/analytics/`)

Representative endpoints:

- `GET /analytics/total-listings/`
- `GET /analytics/total-revenue/`
- `GET /analytics/total-reservations/`
- `GET /analytics/food-waste-reduction/`
- `GET /analytics/total-no-shows/`
- `GET /analytics/collected-reservations/`

### Game (`/game/`)

Representative endpoints:

- `GET /game/api/game/summary/`
- `GET /game/api/game/recent/`

## Frontend Routes (Current)

- `/login`
- `/signup/seller`
- `/signup/user`
- `/seller`
- `/user`
- `/orders`
- `/game`

## Team

Contributors:

- James Clarke
- Jacob Evans
- Harry Price
- Will Brown
- Anna Hedley
- Lucas Parish
- Zac Dowlands

## Project Status

Academic/team project under active development. The current repository prioritizes feature completeness and demonstrable workflows; further hardening and deployment configuration are recommended before production use.
