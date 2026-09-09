from django.test import TestCase, Client
from django.urls import reverse
from .models import Product, Enquiry


class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Herbal Oil",
            category="hair_care",
            description="Pure herbal oil description.",
            price=299.00,
            image="products/test_oil.jpg",
            is_active=True
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), "Test Herbal Oil (₹299.0)")

    def test_whatsapp_url_generation(self):
        url = self.product.get_whatsapp_url(customer_name="Rohan", customer_phone="9876543210")
        self.assertIn("https://wa.me/919778256391", url)
        self.assertIn("Test%20Herbal%20Oil", url)
        self.assertIn("Rohan", url)


class MultiPageAndFormValidationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.product1 = Product.objects.create(
            name="Kumkumadi Face Pack",
            category="face_care",
            description="Radiance saffron pack.",
            price=650.00,
            image="products/face_pack.jpg",
            is_active=True
        )
        self.product2 = Product.objects.create(
            name="KeshVeda Herbal Hair Oil",
            category="hair_care",
            description="Roots strengthening herbal hair oil.",
            price=499.00,
            image="products/hair_oil.jpg",
            is_active=True
        )

    def test_home_page(self):
        response = self.client.get(reverse('backend:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vanam Ayurveda")
        self.assertContains(response, "Kumkumadi Face Pack")
        self.assertContains(response, "Enquire on WhatsApp")

    def test_about_page(self):
        response = self.client.get(reverse('backend:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Art of Taila Paka Vidhi")
        self.assertContains(response, "Western Ghats")

    def test_products_catalog_page(self):
        response = self.client.get(reverse('backend:products'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kumkumadi Face Pack")
        self.assertContains(response, "KeshVeda Herbal Hair Oil")
        self.assertContains(response, "₹ 650.00")
        self.assertContains(response, "₹ 499.00")

    def test_products_category_filter(self):
        response = self.client.get(reverse('backend:products') + '?category=hair_care')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "KeshVeda Herbal Hair Oil")
        self.assertNotContains(response, "Kumkumadi Face Pack")

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
        self.assertContains(response, "Your enquiry for Kumkumadi Face Pack has been received")
        self.assertEqual(Enquiry.objects.count(), 1)
        enquiry = Enquiry.objects.first()
        self.assertEqual(enquiry.name, "Pooja Verma")
        self.assertEqual(enquiry.phone_number, "9876543210")
