# SoleDrop

A modern, full-featured Django-based e-commerce platform for selling footwear online. SoleDrop provides a seamless shopping experience with product management, cart functionality, order processing, and an intuitive admin dashboard.

## Project Overview

SoleDrop is a production-ready e-commerce application built with Django, featuring user authentication, product catalog management, shopping cart, order tracking, coupon management, and an admin dashboard for store management. The platform supports multiple payment methods including Cash on Delivery and online payments.

## Features

### Customer Features
- **User Authentication**: Email-based registration and login with Google OAuth social authentication
- **Product Browsing**: Browse products by category with pagination support
- **Product Details**: View product information, variants (sizes), reviews, and ratings
- **Shopping Cart**: Add/remove items, update quantities, automatic shipping charge calculation
- **Wishlist**: Save favorite products for later
- **Checkout Process**: Multi-step checkout with address selection/creation
- **Order Management**: Track order status (pending, confirmed, shipped, delivered, cancelled)
- **User Profile**: View order history, manage addresses, edit profile information
- **Product Reviews**: Leave ratings and comments on purchased items
- **Coupon System**: Apply discount codes with validation (percentage or fixed amount)

### Admin Features
- **Dashboard**: Overview of sales, orders, revenue, and inventory
- **Product Management**: Create, edit, delete products and manage categories
- **Inventory Management**: Manage product variants (sizes) and stock levels
- **Order Management**: View all orders, update order status, track shipments
- **User Management**: View customer profiles and activity
- **Category Management**: Create and manage product categories
- **Coupon Management**: Create and manage promotional codes with expiration and usage limits
- **Analytics**: View top products, low stock items, and sales metrics

## Tech Stack

### Backend
- **Django** 6.0.3 - Web framework
- **PostgreSQL** - Database
- **Gunicorn** 25.3.0 - WSGI application server
- **Python 3.x** - Programming language

### Authentication & Authorization
- **django-allauth** 65.16.1 - Authentication with email and OAuth
- **PyJWT** 2.12.1 - JWT token handling
- **cryptography** 47.0.0 - Encryption support

### Database & ORM
- **psycopg** 3.3.3 - PostgreSQL adapter
- **dj-database-url** 3.1.2 - Database URL parsing

### Utilities
- **Pillow** 12.1.1 - Image processing
- **python-dotenv** 1.2.2 - Environment variable management
- **django-extensions** 4.1 - Additional Django utilities
- **django-autoslug** 1.9.9 - Automatic slug generation
- **django-mathfilters** 1.0.0 - Template filters for math operations
- **requests** 2.33.1 - HTTP library

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)
- Virtual environment tool (venv or virtualenv)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd soledrop