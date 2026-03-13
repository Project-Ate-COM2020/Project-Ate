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
python manage.py test issue_reporting.tests
```

## API Overview

Base URL: `http://127.0.0.1:8000/`

### Marketplace (`/marketplace/`)

#### Allergens

- `GET /marketplace/allergens/`

#### Bundle Listings

- `POST /marketplace/bundle/`
- `GET /marketplace/bundles/`
- `GET /marketplace/bundles/between`
- `GET /marketplace/bundles/oldest`
- `GET /marketplace/bundles/older/`
- `GET /marketplace/bundles/newer/`
- `GET /marketplace/bundles/open/`
- `GET /marketplace/bundles/collection/`
- `GET /marketplace/bundle/<bundle_id>/`

#### Consumer Profiles

- `POST /marketplace/consumer`
- `GET /marketplace/consumer/<consumer_id>/`
- `PUT /marketplace/consumer/<consumer_id>/`
- `PATCH /marketplace/consumer/<consumer_id>/`
- `DELETE /marketplace/consumer/<consumer_id>/`

#### Seller Profiles (Marketplace domain)

- `POST /marketplace/seller`
- `GET /marketplace/seller/<seller_id>/`
- `PUT /marketplace/seller/<seller_id>/`
- `PATCH /marketplace/seller/<seller_id>/`
- `DELETE /marketplace/seller/<seller_id>/`

#### Seller Bundle Views

- `GET /marketplace/seller/<seller_id>/bundles`
- `GET /marketplace/seller/<seller_id>/bundles/between`
- `GET /marketplace/seller/<seller_id>/bundles/newest`
- `GET /marketplace/seller/<seller_id>/bundles/oldest`
- `GET /marketplace/seller/<seller_id>/bundles/older/`
- `GET /marketplace/seller/<seller_id>/bundles/younger/`
- `GET /marketplace/seller/<seller_id>/bundles/collection/`

#### Reservations

- `POST /marketplace/reservations`
- `GET /marketplace/reservations/<reservation_id>/`
- `PUT /marketplace/reservations/<reservation_id>/`
- `PATCH /marketplace/reservations/<reservation_id>/`
- `DELETE /marketplace/reservations/<reservation_id>/`

#### JWT Authentication

- `POST /marketplace/seller/auth/token`
- `POST /marketplace/seller/auth/token/refresh`
- `POST /marketplace/seller/auth/token/verify/`
- `POST /marketplace/consumer/auth/token`
- `POST /marketplace/consumer/auth/token/refresh`
- `POST /marketplace/consumer/auth/token/verify/`

### Seller (`/seller/`)

- `GET /seller/getsellername/?seller_id=<seller_id>`
- `GET /seller/getselleraddress/?seller_id=<seller_id>`
- `GET /seller/getreservations/?seller_id=<seller_id>`
- `POST /seller/createlisting/`
- `POST /seller/collectbundle/`

### Buyer (`/buyer/`)

- `POST /buyer/reservebundle/`
- `POST /buyer/unreservebundle/`
- `GET /buyer/getreservations/<consumer_id>/`

### Forecasting (`/forecast/`)

- `POST /forecast/prediction/`

Request fields:
- Required: `category`, `day_of_week`, `time_window`
- Optional: `seller_id`, `weather`, `no_bundles`, `price`

### Analytics (`/analytics/`)

All endpoints are `GET` and expect `seller_id` as a query parameter.

- `/analytics/total-listings/`
- `/analytics/total-revenue/`
- `/analytics/total-reservations/`
- `/analytics/food-waste-reduction/`
- `/analytics/total-no-shows/`
- `/analytics/collected-reservations/`
- `/analytics/sell-through/`
- `/analytics/waste-proxy/`
- `/analytics/pricing-effectiveness/`
- `/analytics/popular-categories/`
- `/analytics/best-pickup-windows/`

### Game (`/game/`)

- `GET /game/api/game/summary/`
- `GET /game/api/game/recent/`
- `GET /game/api/test/`

### Maintainer (`/maintainer/`)

- `POST /maintainer/auth/token`
- `POST /maintainer/auth/refresh`
- `POST /maintainer/auth/verify`

### Issue Reporting (`/issues/`)

#### Buyer APIs

- `POST /issues/report/`
- `GET /issues/buyer/<consumer_id>/`
- `GET /issues/buyer/<consumer_id>/reportable-postings/`

#### Seller APIs

- `GET /issues/seller/<seller_id>/`
- `GET /issues/seller/<seller_id>/overview/`
- `PATCH /issues/seller/<seller_id>/<issue_id>/respond/`

### Utility/Framework Endpoints

- `GET|POST /api-auth/` (DRF browsable API auth)
- `GET /admin/` (Django admin)

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
