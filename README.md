# 🌿 AyuDhara — Responsive Ayurvedic Products Website & Custom Admin Dashboard

A production-quality, responsive Ayurvedic personal care web platform built with **Django 6.x**, **HTML5**, **Custom Vanilla CSS3**, and **Vanilla JavaScript** for **AyuDhara**, showcasing handcrafted Ayurvedic personal-care formulations (Hair Oil, Face Pack, Herbal Shampoo, Body Oil) with dynamic database models, server-side validation, WhatsApp business integration, cinematic background video cycling, and a comprehensive **Custom Admin Dashboard** for staff operations.

---

## 📁 Repository & Directory Structure

This project is organized into structured frontend and backend directories:

```
Ayurvedic_Products_website/
│
├── frontend/                     # Frontend templates, styles, scripts, and video assets
│   ├── base.html                 # Master layout template (AyuDhara SVG logo mark, Navigation, Footer, Meta, Tokens)
│   ├── home.html                 # Home page with 3-reel cinematic video background hero & category accents
│   ├── about.html                # About Us page (Heritage, Taila Paka Vidhi, Craft pillars)
│   ├── products.html             # Products catalog page with category filtering (ORM) & 4:3 cards
│   ├── contact.html              # Contact & Enquiry form with 10-digit Indian phone regex validation
│   ├── dashboard/                # Custom Admin Dashboard Templates (Section 6)
│   │   ├── base_dashboard.html   # Persistent sidebar layout & mobile responsive drawer
│   │   ├── login.html            # Dedicated staff authentication portal
│   │   ├── overview.html         # Store Overview with 3 KPI metric cards & quick tables
│   │   ├── product_list.html     # Product management table with stock status badges & WhatsApp links
│   │   ├── product_form.html     # Add & Edit Product form with live JavaScript image preview
│   │   ├── product_confirm_delete.html # Confirmation modal for product deletion
│   │   └── enquiry_list.html     # Customer enquiries table with status workflow toggles
│   ├── css/
│   │   └── style.css             # Vanilla CSS design system (Tone A Ivory, Tone B Sand, Category Top-Borders)
│   ├── js/
│   │   └── main.js               # Multi-video switcher, mobile navigation, dynamic form sync, live image preview
│   └── videos/                   # 3 seamless background videos for hero carousel
│       ├── ayurveda_spices_herbs.mp4
│       ├── ayurveda_oil_ritual.mp4
│       └── ayurveda_dried_botanicals.mp4
│
├── backend/                      # Django backend application package
│   ├── __init__.py
│   ├── apps.py                   # BackendConfig application configuration
│   ├── models.py                 # Product (with stock_quantity, in_stock) & Enquiry (with status workflow)
│   ├── forms.py                  # Public EnquiryForm with 10-digit Indian phone regex validation
│   ├── views.py                  # Multi-page public views (home, about, products, contact)
│   ├── urls.py                   # Public URL routing (namespace 'backend')
│   ├── dashboard_forms.py        # Staff Dashboard LoginForm & ProductForm
│   ├── dashboard_views.py        # Custom Dashboard views (KPI overview, Product CRUD, Enquiry status)
│   ├── dashboard_urls.py         # Dashboard URL routing (namespace 'dashboard')
│   ├── admin.py                  # Django default admin interface with thumbnail preview & WhatsApp actions
│   ├── tests.py                  # Full test suite (16 tests: models, views, forms, and custom dashboard)
│   ├── migrations/               # Database migration files
│   └── management/
│       └── commands/
│           └── seed_products.py  # Management command populating catalog with realistic stock levels
│
├── vanam_project/                # Django project configuration
│   ├── __init__.py
│   ├── settings.py               # Configured for frontend/ templates & staticfiles, media
│   ├── urls.py                   # Main project URL router (/dashboard/ and /)
│   ├── wsgi.py                   # WSGI server gateway
│   └── asgi.py                   # ASGI server gateway
│
├── media/                        # User-uploaded & seeded media
│   └── products/                 # High-resolution Ayurvedic product photography
│       ├── hair_oil.jpg
│       ├── face_pack.jpg
│       ├── shampoo.jpg
│       └── body_oil.jpg
│
├── manage.py                     # Django management script
├── requirements.txt              # Project dependencies (Django, Pillow)
├── .gitignore                    # Version control ignore rules
└── README.md                     # Documentation & setup guide
```

---

## 🌟 Key Features & Specifications Met

### 1. Brand Identity & Visual Design System (Section 5)
- **Brand Name**: **AyuDhara** ("Flow of Life").
- **Custom Vector Logo**: Hand-crafted SVG flowing stream resolving into a sacred leaf with a warm Turmeric gold accent tip.
- **Two-Tone Wordmark**: "Ayu" rendered in deep Forest Green (`#1F3327`) and "Dhara" in warm Turmeric Gold (`#B78103`).
- **Curated Color Palette**:
  - Tone A (Ivory Ground): `#FBF7EF`
  - Tone B (Sand Container): `#F1E9D6`
  - Deep Forest Green: `#1F3327` / Dark Slate: `#14221A`
  - Category Top-Borders: Hair Care (`#1B7A5E`), Face Care (`#E8674A`), Body Care (`#C4562F`), Wellness (`#C97F00`).
- **Standardized Product Cards**: 4:3 aspect ratio images with smooth zoom hover transitions, clear pricing, and prominent WhatsApp enquiry buttons.

### 2. Multi-Page Public Website
- **Home (`/`)**: Cinematic hero banner sequentially cycling through 3 botanical video reels (with non-blocking 7-second timers and bottom breathing room), brand pillars, and featured formulations.
- **About (`/about/`)**: Heritage storytelling from Wayanad, Kerala, the classical 21-day *Taila Paka Vidhi* decoction technique, and ethical sourcing standards.
- **Products Catalog (`/products/`)**: Dynamic ORM query filtering with active category pills, price badges in ₹, and stock status indicators.
- **Contact & Enquiry (`/contact/`)**: Real-time validation for 10-digit Indian mobile numbers (`^[6-9]\d{9}$`), dynamic message encoding, and immediate feedback banners.

### 3. WhatsApp Business Integration
- **Direct Business Line**: `97782 56391` (`+91 97782 56391`).
- Custom URLs generated automatically on `Product` and `Enquiry` models using `get_whatsapp_url()`, pre-populating formulation name, price, category, and customer queries.
- Official WhatsApp vector badge on buttons.

### 4. Custom Admin Dashboard (`/dashboard/`)
- **Dedicated Staff Portal**: Accessible at `/dashboard/login/` (staff authentication enforced).
- **Executive KPI Analytics**:
  - Active Formulations live in catalog.
  - Stock Alerts (items with $\le 5$ units or out of stock).
  - Total Enquiries received.
- **Full Product CRUD**: Add, edit, list, and delete products with live JavaScript image previews.
- **Enquiry Workflow Management**: Update inquiry status between `New`, `Contacted`, and `Resolved`, with direct one-click WhatsApp client launch buttons.
- **Mobile Responsive**: Off-canvas sliding sidebar drawer for phone screens.

---

## 🚀 Setup & Execution Guide

### 1. Dependencies & Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# macOS / Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Apply Migrations & Seed Products
```bash
python manage.py makemigrations backend
python manage.py migrate
python manage.py seed_products
```

### 3. Run Development Server
```bash
python manage.py runserver
```
- Public Website: **`http://127.0.0.1:8000/`**
- Custom Admin Dashboard: **`http://127.0.0.1:8000/dashboard/`**
- Django Default Admin: **`http://127.0.0.1:8000/admin/`**

---

## 🔑 Default Credentials
- **Username**: `admin`
- **Password**: `adminpassword123`

---

## 🧪 Running Automated Tests
```bash
python manage.py test
```
All **16 automated test cases** cover model properties, WhatsApp URL generation, public page rendering, category filtering, 10-digit phone regex validation, custom dashboard permissions, product CRUD, and enquiry status transitions.
