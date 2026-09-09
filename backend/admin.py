from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Enquiry


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'category', 'price', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_active')
    readonly_fields = ('image_preview_large', 'created_at', 'updated_at')

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 6px; border: 1px solid #ccc;" />',
                obj.image.url
            )
        return format_html('<span style="color: #999;">No image</span>')
    image_preview.short_description = "Thumbnail"

    def image_preview_large(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 250px; height: auto; border-radius: 8px; border: 1px solid #ccc;" />',
                obj.image.url
            )
        return format_html('<span style="color: #999;">No image uploaded yet</span>')
    image_preview_large.short_description = "Image Preview"


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'product', 'is_processed', 'created_at', 'whatsapp_action')
    list_filter = ('is_processed', 'created_at', 'product__category')
    search_fields = ('name', 'phone_number', 'message', 'product__name')
    list_editable = ('is_processed',)
    readonly_fields = ('created_at',)

    def whatsapp_action(self, obj):
        url = obj.get_whatsapp_url()
        return format_html(
            '<a href="{}" target="_blank" style="background-color: #25D366; color: white; padding: 4px 10px; border-radius: 4px; text-decoration: none; font-weight: bold; display: inline-block;">📱 Open WhatsApp</a>',
            url
        )
    whatsapp_action.short_description = "WhatsApp Action"
