from django.db import models
from django.conf import settings
import urllib.parse


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('hair_care', 'Hair Care'),
        ('face_care', 'Face & Skincare'),
        ('body_care', 'Body & Bath'),
        ('wellness', 'Wellness / General'),
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
    stock_quantity = models.PositiveIntegerField(
        default=25,
        help_text="Available inventory count in units"
    )
    is_active = models.BooleanField(
        default=True, 
        help_text="Uncheck to hide product from site"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.name} (₹{self.price})"

    @property
    def in_stock(self):
        """Derived in-stock status based on stock_quantity and is_active flag."""
        return self.is_active and self.stock_quantity > 0

    @property
    def stock_status(self):
        """Helper property for badge coloring: 'out_of_stock', 'low_stock', or 'in_stock'."""
        if not self.is_active or self.stock_quantity == 0:
            return 'out_of_stock'
        elif self.stock_quantity <= 5:
            return 'low_stock'
        return 'in_stock'

    def get_whatsapp_url(self, customer_name=None, customer_phone=None, message=None):
        """
        Generates dynamic wa.me link with encoded enquiry message for this product.
        """
        biz_number = getattr(settings, 'WHATSAPP_BUSINESS_NUMBER', '919778256391')
        
        text = f"Namaste AyuDhara! 🙏\n\nI would like to enquire about your continuous heritage formulation:\n📦 *{self.name}*\n💰 Price: ₹{self.price}\n🏷️ Category: {self.get_category_display()}\n"
        
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
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('resolved', 'Resolved'),
    ]

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
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name="Enquiry Status",
        help_text="Track enquiry progress as an informal order"
    )
    is_processed = models.BooleanField(default=False, verbose_name="Status Processed")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Customer Enquiry"
        verbose_name_plural = "Customer Enquiries"

    def __str__(self):
        prod_name = self.product.name if self.product else "General Enquiry"
        return f"Enquiry from {self.name} for {prod_name} [{self.get_status_display()}]"

    def get_whatsapp_url(self):
        biz_number = getattr(settings, 'WHATSAPP_BUSINESS_NUMBER', '919778256391')
        if self.product:
            return self.product.get_whatsapp_url(
                customer_name=self.name,
                customer_phone=self.phone_number,
                message=self.message
            )
        else:
            text = f"Namaste AyuDhara! 🙏\n\nI have an enquiry:\n👤 Name: {self.name}\n📞 Phone: {self.phone_number}\n💬 Message: {self.message}"
            return f"https://wa.me/{biz_number}?text={urllib.parse.quote(text)}"
