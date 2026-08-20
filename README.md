# ShopEase

ShopEase is a lightweight, Python-backed web storefront designed for small businesses to list products, accept orders, and process payments through a clean, responsive HTML/CSS interface. It combines a Python backend (Flask) with semantic HTML and Bootstrap-based frontend components to deliver a simple, extensible shopping experience. The project focuses on core e-commerce functionality—product catalog, shopping cart, checkout, and an admin dashboard—while keeping the codebase easy to understand and adapt. ShopEase is suitable as a starter template for learning web development or as the foundation for a production-ready store after further hardening and integration.

## Technologies Used
- Python (Flask web framework)
- HTML5, CSS3, Bootstrap for responsive UI
- Jinja2 templating
- SQLite (default) / PostgreSQL (production-ready option)
- SQLAlchemy (ORM)
- Flask-Login (authentication)
- Flask-Migrate / Alembic (database migrations)
- Stripe (payments) — integration placeholder
- Docker & docker-compose (optional containerized deployment)
- GitHub Actions (CI/CD)
- pytest (unit and integration tests)

## Features
- Product Catalog
  - List, categorize, and view product detail pages with images, descriptions, SKU, price and stock info.
- Full-text Search & Filters
  - Search products by name/description and filter by category, price range, or availability.
- Shopping Cart
  - Add/remove items, update quantities, and preserve cart per-user using session or account storage.
- Checkout Flow
  - Address collection, order summary, tax/shipping estimates, and payment processing via Stripe (or a configured provider).
- User Authentication & Profiles
  - User registration, login/logout, password reset, and a profile page with order history.
- Admin Dashboard
  - Secure admin interface for creating/editing products, viewing orders, and managing inventory.
- Order Management
  - Create, update, and track order status (pending, paid, fulfilled, cancelled) with email notifications.
- RESTful API Endpoints
  - API for product listings, cart operations, and order creation to enable headless or mobile frontends.
- Responsive Design & Accessibility
  - Mobile-first layout powered by Bootstrap, with ARIA attributes and keyboard navigation considerations.
- Tests & CI/CD
  - Unit and integration tests using pytest and a GitHub Actions workflow for automated checks.
- Docker Support
  - Optional Docker and docker-compose setup for consistent dev and staging environments.

## Process / Architecture
ShopEase was built using a modular approach to keep frontend and backend responsibilities clear. The backend uses Flask with SQLAlchemy for data modeling, and Flask blueprints separate user, product, and admin routes. Templates are rendered server-side with Jinja2 for initial pages, while AJAX endpoints provide dynamic cart and search interactions. Database migrations are managed with Flask-Migrate so schema changes remain reproducible. The frontend leverages Bootstrap for responsive components and a simple, accessible UI. Payments are abstracted behind a service layer so Stripe or another provider can be swapped with minimal changes. The project emphasizes readability and testability: core business logic is encapsulated in services and model methods, and automated tests validate critical flows (cart, checkout, and authentication). Dockerfiles and a docker-compose.yml provide optional containerization for development and CI runs.

## How to run 
1. Prerequisites
   - Install Python 3.10+ and Git.
   - (Optional) Install Docker & docker-compose if you prefer containerized runs.

2. Clone the repository
   - git clone https://github.com/ayen-123/ShopEase.git
   - cd ShopEase

3. Create and activate a virtual environment
   - python -m venv .venv
   - source .venv/bin/activate   (Windows: .venv\Scripts\activate)

4. Install dependencies
   - pip install --upgrade pip
   - pip install -r requirements.txt

5. Set environment variables (example)
   - export FLASK_APP=run.py
   - export FLASK_ENV=development
   - export SECRET_KEY='your-secret-key'
   - export DATABASE_URL='sqlite:///shop.db'  # or your PostgreSQL URI
   - export STRIPE_API_KEY='sk_test_...'      # if using Stripe

6. Initialize the database
   - flask db init        # only the first time
   - flask db migrate -m "Initial migration"
   - flask db upgrade

   Or if your project seeds a DB script:
   - python scripts/seed_db.py

7. Create an admin user
   - python manage.py create-admin --email admin@example.com
   (or use the registration flow in the app)

8. Run the development server
   - flask run
   - Open http://127.0.0.1:5000 in your browser

9. Run tests
   - pytest




