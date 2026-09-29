from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from .models import Product, Enquiry
from .forms import EnquiryForm


def home_view(request):
    """
    Home page view: Video hero banner, Brand ethos, Featured products showcase, and quick contact teaser.
    """
    featured_products = Product.objects.filter(is_active=True).order_by('-created_at')[:4]
    
    context = {
        'featured_products': featured_products,
        'whatsapp_business_number': getattr(settings, 'WHATSAPP_DISPLAY_NUMBER', '+91 80753 19502'),
    }
    return render(request, 'home.html', context)


def about_view(request):
    """
    Dedicated About Us page: Brand heritage, Taila Paka Vidhi, organic harvesting principles.
    """
    context = {
        'whatsapp_business_number': getattr(settings, 'WHATSAPP_DISPLAY_NUMBER', '+91 80753 19502'),
    }
    return render(request, 'about.html', context)


def products_view(request):
    """
    Dedicated Products catalog page:
    - Lists products with dynamic ORM querying
    - Supports filtering by category
    """
    category = request.GET.get('category', '').strip()
    products = Product.objects.filter(is_active=True).order_by('-created_at')

    if category:
        products = products.filter(category=category)

    categories = Product.CATEGORY_CHOICES

    context = {
        'products': products,
        'selected_category': category,
        'categories': categories,
        'whatsapp_business_number': getattr(settings, 'WHATSAPP_DISPLAY_NUMBER', '+91 80753 19502'),
    }
    return render(request, 'products.html', context)


def product_detail_view(request, pk):
    """
    Dedicated Product Details page:
    - Displays detailed product information, high-res image, ingredients, benefits, stock status
    - Direct WhatsApp link and Send Enquiry form integration
    - Shows related formulations in the same category
    """
    product = get_object_or_404(Product, pk=pk, is_active=True)
    related_products = Product.objects.filter(is_active=True, category=product.category).exclude(pk=product.pk)[:3]

    context = {
        'product': product,
        'related_products': related_products,
        'whatsapp_business_number': getattr(settings, 'WHATSAPP_DISPLAY_NUMBER', '+91 80753 19502'),
    }
    return render(request, 'product_detail.html', context)


def contact_view(request):
    """
    Dedicated Contact & Enquiry page:
    - Customer enquiry form with server-side phone regex validation
    - Pre-populates selected product if query param ?product_id=... is present
    - Inline error messaging and success confirmation
    """
    initial_data = {}
    selected_product_id = request.GET.get('product_id')
    if selected_product_id and selected_product_id.isdigit():
        try:
            initial_data['product'] = Product.objects.get(pk=int(selected_product_id), is_active=True)
        except Product.DoesNotExist:
            pass

    whatsapp_url = None
    form_submitted = False

    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save()
            form_submitted = True
            whatsapp_url = enquiry.get_whatsapp_url()
            messages.success(
                request,
                f"Thank you, {enquiry.name}! Your enquiry for {enquiry.product.name} has been received. Our wellness consultant will connect with you shortly."
            )
            form = EnquiryForm()
    else:
        form = EnquiryForm(initial=initial_data)

    context = {
        'form': form,
        'form_submitted': form_submitted,
        'whatsapp_url': whatsapp_url,
        'whatsapp_business_number': getattr(settings, 'WHATSAPP_DISPLAY_NUMBER', '+91 80753 19502'),
    }
    return render(request, 'contact.html', context)
