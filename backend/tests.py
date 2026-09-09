from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Enquiry


class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Herbal Oil",
            category="hair_care",
            description="Pure herbal oil description.",
            price=299.00,
            stock_quantity=20,
            image="products/test_oil.jpg",
            is_active=True
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), "Test Herbal Oil (₹299.0)")

    def test_in_stock_property(self):
        self.assertTrue(self.product.in_stock)
        self.assertEqual(self.product.stock_status, 'in_stock')

        self.product.stock_quantity = 3
        self.assertEqual(self.product.stock_status, 'low_stock')

        self.product.stock_quantity = 0
        self.assertFalse(self.product.in_stock)
        self.assertEqual(self.product.stock_status, 'out_of_stock')

    def test_whatsapp_url_generation(self):
        url = self.product.get_whatsapp_url(customer_name="Rohan", customer_phone="9876543210")
        self.assertIn("https://wa.me/919778256391", url)
        self.assertIn("AyuDhara", url)
        self.assertIn("Test%20Herbal%20Oil", url)
        self.assertIn("Rohan", url)


class PublicPagesAndValidationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.product1 = Product.objects.create(
            name="Kumkumadi Radiant Face Pack",
            category="face_care",
            description="Radiance saffron pack.",
            price=650.00,
            stock_quantity=15,
            image="products/face_pack.jpg",
            is_active=True
        )
        self.product2 = Product.objects.create(
            name="KeshVeda Herbal Hair Oil",
            category="hair_care",
            description="Roots strengthening herbal hair oil.",
            price=499.00,
            stock_quantity=25,
            image="products/hair_oil.jpg",
            is_active=True
        )

    def test_home_page(self):
        response = self.client.get(reverse('backend:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "AyuDhara")
        self.assertContains(response, "Kumkumadi Radiant Face Pack")
        self.assertContains(response, "Enquire on WhatsApp")

    def test_about_page(self):
        response = self.client.get(reverse('backend:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "AyuDhara")
        self.assertContains(response, "The Art of Taila Paka Vidhi")
        self.assertContains(response, "Western Ghats")

    def test_products_catalog_page(self):
        response = self.client.get(reverse('backend:products'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kumkumadi Radiant Face Pack")
        self.assertContains(response, "KeshVeda Herbal Hair Oil")
        self.assertContains(response, "₹ 650.00")
        self.assertContains(response, "₹ 499.00")

    def test_products_category_filter(self):
        response = self.client.get(reverse('backend:products') + '?category=hair_care')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "KeshVeda Herbal Hair Oil")
        self.assertNotContains(response, "Kumkumadi Radiant Face Pack")

    def test_contact_page_get(self):
        response = self.client.get(reverse('backend:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Connect with Our Ayurvedic Wellness Desk")
        self.assertContains(response, "Send an Official Product Enquiry")

    def test_contact_form_invalid_phone(self):
        response = self.client.post(reverse('backend:contact'), {
            'name': 'Ramesh Kumar',
            'phone_number': '1234',
            'product': self.product1.id,
            'message': 'Need details'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a valid 10-digit Indian phone number")
        self.assertEqual(Enquiry.objects.count(), 0)

    def test_contact_form_valid_submission(self):
        response = self.client.post(reverse('backend:contact'), {
            'name': 'Pooja Verma',
            'phone_number': '9876543210',
            'product': self.product1.id,
            'message': 'Interested in buying 2 face packs.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your enquiry for Kumkumadi Radiant Face Pack has been received")
        self.assertEqual(Enquiry.objects.count(), 1)
        enquiry = Enquiry.objects.first()
        self.assertEqual(enquiry.name, "Pooja Verma")
        self.assertEqual(enquiry.phone_number, "9876543210")
        self.assertEqual(enquiry.status, 'new')


class CustomAdminDashboardTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username="teststaff",
            password="securepassword123",
            is_staff=True
        )
        self.normal_user = User.objects.create_user(
            username="normaluser",
            password="normalpassword123",
            is_staff=False
        )
        self.product = Product.objects.create(
            name="Test Face Pack",
            category="face_care",
            description="Organic radiant clay mask.",
            price=350.00,
            stock_quantity=4,
            image="products/test_mask.jpg",
            is_active=True
        )
        self.enquiry = Enquiry.objects.create(
            name="Ananya Sen",
            phone_number="9876543210",
            product=self.product,
            message="Looking for urgent delivery to Mumbai.",
            status="new"
        )

    def test_dashboard_unauthenticated_redirect(self):
        response = self.client.get(reverse('dashboard:overview'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('dashboard:login'), response.url)

    def test_dashboard_login_page_renders(self):
        response = self.client.get(reverse('dashboard:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Staff Admin Desk")
        self.assertContains(response, "AyuDhara")

    def test_dashboard_login_success(self):
        response = self.client.post(reverse('dashboard:login'), {
            'username': 'teststaff',
            'password': 'securepassword123',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Store Overview")

    def test_dashboard_overview_kpis(self):
        self.client.login(username='teststaff', password='securepassword123')
        response = self.client.get(reverse('dashboard:overview'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Active Formulations")
        self.assertContains(response, "Stock Alerts")
        self.assertContains(response, "Ananya Sen")

    def test_dashboard_product_crud(self):
        self.client.login(username='teststaff', password='securepassword123')

        # List
        response = self.client.get(reverse('dashboard:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Face Pack")

        # Edit
        response = self.client.post(reverse('dashboard:product_edit', args=[self.product.id]), {
            'name': 'Updated Face Pack',
            'category': 'face_care',
            'price': '399.00',
            'stock_quantity': '30',
            'description': 'Updated description.',
            'is_active': True,
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Face Pack')
        self.assertEqual(self.product.stock_quantity, 30)

        # Delete
        response = self.client.post(reverse('dashboard:product_delete', args=[self.product.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

    def test_dashboard_enquiry_status_transition(self):
        self.client.login(username='teststaff', password='securepassword123')
        
        # Transition new -> contacted
        response = self.client.post(reverse('dashboard:enquiry_status_update', args=[self.enquiry.id]), {
            'status': 'contacted'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.enquiry.refresh_from_db()
        self.assertEqual(self.enquiry.status, 'contacted')

        # Transition contacted -> resolved
        response = self.client.post(reverse('dashboard:enquiry_status_update', args=[self.enquiry.id]), {
            'status': 'resolved'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.enquiry.refresh_from_db()
        self.assertEqual(self.enquiry.status, 'resolved')
        self.assertTrue(self.enquiry.is_processed)
