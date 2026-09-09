# 🌿 Vanam Ayurveda - Responsive Ayurvedic Products Website

A production-quality, responsive Ayurvedic personal care website built with **Django 6.x**, **HTML5**, **Custom Vanilla CSS3**, and **Vanilla JavaScript** for **Vanam Ayurveda**, showcasing handcrafted Ayurvedic personal-care products (Hair Oil, Face Pack, Herbal Shampoo, Body Oil) with dynamic database models, server-side validation, WhatsApp business integration, and cinematic hero video switcher.

---

## 📁 Repository & Directory Structure

This project is organized into structured frontend and backend directories:

```
Ayurvedic_Products_website/
│
├── frontend/                     # Frontend templates, styles, scripts, and video assets
│   ├── base.html                 # Master layout template (Navigation, Footer, Meta, Tokens)
│   ├── home.html                 # Home page with 3-reel cinematic video background hero
│   ├── about.html                # About Us page (Heritage, Taila Paka Vidhi, Craft pillars)
│   ├── products.html             # Products catalog page with category filtering (ORM)
│   ├── contact.html              # Contact & Enquiry form with inline phone validation
│   ├── css/
│   │   └── style.css             # Vanilla CSS design system (Variables, Grid, Typography)
│   ├── js/
│   │   └── main.js               # Multi-video switcher reel, mobile menu, dynamic form sync
│   └── videos/                   # 3 seamless background videos for hero carousel
│       ├── ayurveda_spices_herbs.mp4
│       ├── ayurveda_oil_ritual.mp4
│       └── ayurveda_dried_botanicals.mp4
│
├── backend/                      # Django backend application package
│   ├── __init__.py
│   ├── apps.py                   # BackendConfig application configuration
│   ├── models.py                 # Product and Enquiry models with get_whatsapp_url()
│   ├── forms.py                  # EnquiryForm with 10-digit Indian phone regex validation
│   ├── views.py                  # Multi-page views (home, about, products, contact)
│   ├── urls.py                   # URL routing (namespace 'backend')
│   ├── admin.py                  # Custom admin interface with thumbnail preview & WhatsApp actions
│   ├── tests.py                  # Full test suite (models, views, form validations, filters)
│   ├── migrations/               # Database migration files
│   └── management/
│       └── commands/
│           └── seed_products.py  # Management command to populate initial product catalog
│
├── vanam_project/                # Django project configuration
│   ├── __init__.py
│   ├── settings.py               # Configured for frontend/ templates & staticfiles, media
│   ├── urls.py                   # Main project URL router
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

## 🌟 Key Features & Requirements Met

### 1. Multi-Page Architecture (`frontend/`)
- **Home Page (`/`)**: Features a cinematic multi-video hero banner cycling sequentially across 3 high-definition botanical video reels, brand ethos teaser, featured collection showcase, and direct contact callouts.
- **About Us Page (`/about/`)**: Explains the heritage story from Wayanad, Kerala, the classical 21-day *Taila Paka Vidhi* decoction technique, and the 3 craft pillars.
- **Our Products Page (`/products/`)**: Dynamic ORM catalog with interactive category filters (`hair_care`, `face_care`, `body_care`), price tags in ₹, and quick enquiry triggers.
- **Contact & Enquiry Page (`/contact/`)**: Comprehensive enquiry form with real-time sync to WhatsApp, server-side validation, inline error messaging, and estate location details.

### 2. WhatsApp Business Integration
- Configured centrally in `vanam_project/settings.py` (`WHATSAPP_BUSINESS_NUMBER = '919778256391'`).
- Official WhatsApp vector SVG icons on all enquiry actions.
- Automatic message encoding with product name, price, category, and customer queries.

### 3. Django Backend & Database (`backend/`)
- **`Product` Model**: Category choices, description, pricing in INR, `ImageField`, active status, and custom `get_whatsapp_url()`.
- **`Enquiry` Model**: Stores name, phone number, selected product, message, processed status, and timestamps.
- **`EnquiryForm` Validation**: Regex validator strictly enforcing valid 10-digit Indian phone numbers (`^(?:\+?91)?[6-9]\d{9}$`).

### 4. Admin Management Interface (`/admin/`)
- Registered models with image thumbnail previews, list editable fields, search capabilities, filters, and one-click WhatsApp client contact buttons.

---

## 🚀 Setup & Execution Guide

### 1. Dependencies & Virtual Environment
```bash
# Create virtual environment (if not already created)
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
Visit **`http://127.0.0.1:8000/`** in your browser.

---

## 🔑 Admin Credentials
- **URL**: `http://127.0.0.1:8000/admin/`
- **Username**: `admin`
- **Password**: `adminpassword123`

---

## 🧪 Running Automated Tests
```bash
python manage.py test
```
All tests verify model creation, URL reversing, category filtering, and regex validation.
