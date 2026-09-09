from django.db import models
from django.conf import settings
import urllib.parse


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('hair_care', 'Hair Care'),
        ('face_care', 'Face & Skincare'),
        ('body_care', 'Body & Bath Care'),
        ('wellness', 'Herbal Wellness'),
    ]

    name = models.CharField(max_length=150, help_text="Name of the Ayurvedic product")
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES, 
        default='hair_care',
        help_text="Product category"
    )
    description = models.TextField(help_text="Detailed description of ingredients, benefits, and usage")
    price = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        help_text="Price in INR (₹)"
    )
    image = models.ImageField(
        upload_to='products/', 
        help_text="Upload a clear product photograph"
    )
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide product from site")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.name} (₹{self.price})"

    def get_whatsapp_url(self, customer_name=None, customer_phone=None, message=None):
        """
        Generates dynamic wa.me link with encoded enquiry message for this product.
        """
        biz_number = getattr(settings, 'WHATSAPP_BUSINESS_NUMBER', '919778256391')
        
        text = f"Namaste Vanam Ayurveda! 🙏\n\nI would like to enquire about your product:\n📦 *{self.name}*\n💰 Price: ₹{self.price}\n🏷️ Category: {self.get_category_display()}\n"
        
        if customer_name:
            text += f"\n👤 Customer Name: {customer_name}"
        if customer_phone:
            text += f"\n📞 Phone: {customer_phone}"
        if message:
            text += f"\n💬 Note/Question: {message}"
            
        text += "\n\nPlease let me know about availability and delivery details. Thank you!"
        
        encoded_text = urllib.parse.quote(text)
        return f"https://wa.me/{biz_number}?text={encoded_text}"


class Enquiry(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='enquiries',
        verbose_name="Requested Product"
    )
    name = models.CharField(max_length=100, verbose_name="Customer Name")
    phone_number = models.CharField(max_length=20, verbose_name="Phone Number")
    message = models.TextField(blank=True, verbose_name="Message / Query")
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False, verbose_name="Status Processed")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Customer Enquiry"
        verbose_name_plural = "Customer Enquiries"

    def __str__(self):
        prod_name = self.product.name if self.product else "General Enquiry"
        return f"Enquiry from {self.name} for {prod_name}"

    def get_whatsapp_url(self):
        if self.product:
            return self.product.get_whatsapp_url(
                customer_name=self.name,
                customer_phone=self.phone_number,
                message=self.message
            )
        else:
            biz_number = getattr(settings, 'WHATSAPP_BUSINESS_NUMBER', '919778256391')
            text = f"Namaste Vanam Ayurveda! 🙏\n\nI have an enquiry:\n👤 Name: {self.name}\n📞 Phone: {self.phone_number}\n💬 Message: {self.message}"
            return f"https://wa.me/{biz_number}?text={urllib.parse.quote(text)}"
