# E-Commerce Backend API

A RESTful API for a small e-commerce system built with Django and Django REST Framework. This project demonstrates backend development skills including database modeling, API design, authentication, authorization, and business logic implementation.

## Table of Contents

- [Features](#features)
- [Installation & Setup](#installation--setup)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Architectural Decisions](#architectural-decisions)
- [Assumptions](#assumptions)


---

## Features

### Core Features
- ✅ **User Authentication**: JWT-based authentication with email as username
- ✅ **Product Management**: Full CRUD operations for products
- ✅ **Order Management**: Create orders with multiple items
- ✅ **Stock Validation**: Automatic stock availability checking
- ✅ **Nested Serializers**: Order details include product information
- ✅ **Authorization**: Users can only view their own orders

### Bonus Features
- ✅ **Stock Deduction**: Automatic stock reduction when orders are created
- ✅ **Order Cancellation**: Cancel orders with automatic stock rollback
- ✅ **Django Signals**: Simulated notifications for order events
- ✅ **Filtering & Search**: Product filtering by price/stock, search by name
- ✅ **Pagination**: Paginated responses for products and orders
- ✅ **Query Optimization**: Uses `select_related` and `prefetch_related`

---

## Installation & Setup

### Prerequisites
- Python 3.13.5
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository
```bash
git clone <your-repository-url>
cd ecommerce_backend
```

### Step 2: Create Virtual Environment


### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```


### Step 4: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 6: Run Development Server
```bash
python manage.py runserver
```

The API will be available at: `http://127.0.0.1:8000/`

---

## 📡 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | Register new user | No |
| POST | `/api/auth/login/` | Login & get JWT tokens | No |
| POST | `/api/auth/token/refresh/` | Refresh access token | No |
| GET | `/api/auth/profile/` | Get user profile | Yes |

### Product Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/products/` | List all products | No |
| POST | `/api/products/` | Create new product | Yes (Admin) |
| GET | `/api/products/<id>/` | Get product details | No |
| PUT | `/api/products/<id>/` | Update product | Yes (Admin) |
| DELETE | `/api/products/<id>/` | Delete product | Yes (Admin) |

**Query Parameters:**
- `?search=laptop` - Search products by name/description
- `?price__gte=100` - Filter by minimum price
- `?price__lte=1000` - Filter by maximum price
- `?stock__gte=5` - Filter by minimum stock
- `?ordering=-price` - Order by price (descending)

### Order Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/orders/` | List user's orders | Yes |
| POST | `/api/orders/` | Create new order | Yes |
| GET | `/api/orders/<id>/` | Get order details | Yes (Own orders) |
| POST | `/api/orders/<id>/cancel/` | Cancel order | Yes (Own orders) |

---

## Authentication

This API uses **JWT (JSON Web Token)** authentication.

### 1. Register a User
```bash
POST /api/auth/register/

```

### 2. Login to Get Tokens
```bash
POST /api/auth/login/

```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```
---

## Testing

### Manual Testing with DRF Browsable API
1. Start the server: `python manage.py runserver`
2. Visit: `http://127.0.0.1:8000/api/`
3. Login using the web interface
4. Test endpoints directly in the browser

---

## Architectural Decisions

### 1. Custom User Model
**Decision:** Used email as the primary authentication field instead of username.

**Rationale:**
- Modern UX practice - users prefer email login
- Easier to remember than arbitrary usernames
- Implemented from the start to avoid migration issues

### 2. ViewSets with Routers
**Decision:** Used DRF ViewSets with DefaultRouter instead of function-based views.

**Rationale:**
- Automatic URL generation for CRUD operations
- Less boilerplate code
- Consistent REST API design
- Easy to extend with custom actions (e.g., order cancellation)

### 3. Nested Serializers
**Decision:** Used nested serializers for order details with product information.

**Rationale:**
- Single API call returns complete order information
- Better frontend performance (fewer requests)
- Clear data structure for clients

### 4. Stock Management with Transactions
**Decision:** Used `@transaction.atomic` for order creation and cancellation.

**Rationale:**
- Ensures data consistency (all-or-nothing)
- Prevents race conditions in concurrent requests
- Automatic rollback on errors

### 5. Permissions System
**Decision:** Implemented custom permissions (`IsOrderOwner`, `IsAdminOrReadOnly`).

**Rationale:**
- Fine-grained access control
- Users can only access their own orders
- Admin has full access for management
- Public can browse products

### 6. Query Optimization
**Decision:** Used `select_related` and `prefetch_related` in querysets.

**Rationale:**
- Reduces database queries (N+1 problem)
- Better performance for list views
- Faster API response times

### 7. Price Snapshot in OrderItem
**Decision:** Store product price at time of order, not reference current price.

**Rationale:**
- Historical accuracy for invoices
- Price changes don't affect past orders
- Audit trail for transactions

---

## Assumptions

1. **Single Currency:** All prices are in USD (no multi-currency support)

2. **Stock Management:** 
   - Stock is managed at product level (no warehouse locations)
   - Negative stock is prevented by validation
   - Concurrent order handling uses database-level locking

3. **Order Lifecycle:**
   - Orders start with "pending" status
   - Only pending/confirmed orders can be cancelled
   - No partial cancellations (cancel entire order)

4. **Authentication:**
   - Email is unique across all users
   - Password must be at least 8 characters
   - No password reset functionality (can be added)

5. **Product Management:**
   - Only staff/admin users can create/update/delete products
   - All users (including anonymous) can view products
   - No product categories or images (basic implementation)

6. **Notifications:**
   - Currently simulated with console logs
   - In production, would integrate with email service (SendGrid, AWS SES)

7. **Pagination:**
   - Default page size is 10 items
   - Can be adjusted in settings

8. **Database:**
   - SQLite for development/testing
   - PostgreSQL  for production
   - No database backups configured (should be added)

---

## License

This project is created for educational/assessment purposes.

---

##  Author

**Fardeen Khan**
- Email: fardeenmahar0070@gmail.com




