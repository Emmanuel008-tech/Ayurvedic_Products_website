from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Product, Enquiry
from .dashboard_forms import DashboardLoginForm, ProductForm


def dashboard_login_view(request):
    """
    Custom styled login view for AyuDhara staff dashboard.
    """
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('dashboard:overview')

    if request.method == 'POST':
        form = DashboardLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_staff:
                login(request, user)
                messages.success(request, f"Welcome back to AyuDhara Staff Desk, {user.username}!")
                next_url = request.GET.get('next') or 'dashboard:overview'
                return redirect(next_url)
            else:
                messages.error(request, "Invalid staff credentials or account does not have staff permissions.")
    else:
        form = DashboardLoginForm()

    return render(request, 'dashboard/login.html', {'form': form})


def dashboard_logout_view(request):
    """
    Logs out staff user and redirects to dashboard login.
    """
    logout(request)
    messages.info(request, "You have been logged out of AyuDhara Staff Desk.")
    return redirect('dashboard:login')


@staff_member_required(login_url='dashboard:login')
def dashboard_overview_view(request):
    """
    Dashboard Overview (Section 6.3):
    KPI summary cards + recent enquiries and stock alerts.
    """
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    low_stock_products = Product.objects.filter(stock_quantity__lte=5, is_active=True)
    low_stock_count = low_stock_products.count()
    
    total_enquiries = Enquiry.objects.count()
    new_enquiries = Enquiry.objects.filter(status='new')
    new_enquiries_count = new_enquiries.count()

    recent_enquiries = Enquiry.objects.select_related('product').order_by('-created_at')[:8]

    context = {
        'total_products': total_products,
        'active_products': active_products,
        'low_stock_count': low_stock_count,
        'total_enquiries': total_enquiries,
        'new_enquiries_count': new_enquiries_count,
        'recent_enquiries': recent_enquiries,
        'low_stock_products': low_stock_products[:5],
    }
    return render(request, 'dashboard/overview.html', context)


@staff_member_required(login_url='dashboard:login')
def dashboard_product_list_view(request):
    """
    Products list view (Section 6.4):
    Interactive data table/cards with category filters, stock badges, search, and action buttons.
    """
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    stock_filter = request.GET.get('stock', '').strip()

    products = Product.objects.all().order_by('-created_at')

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if category:
        products = products.filter(category=category)

    if stock_filter == 'low':
        products = products.filter(stock_quantity__gt=0, stock_quantity__lte=5)
    elif stock_filter == 'out':
        products = products.filter(stock_quantity=0)
    elif stock_filter == 'in':
        products = products.filter(stock_quantity__gt=5)

    context = {
        'products': products,
        'query': query,
        'category': category,
        'stock_filter': stock_filter,
        'categories': Product.CATEGORY_CHOICES,
    }
    return render(request, 'dashboard/product_list.html', context)


@staff_member_required(login_url='dashboard:login')
def dashboard_product_add_view(request):
    """
    Add product view (Section 6.4):
    Styled form with image file upload.
    """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Product '{product.name}' was created successfully!")
            return redirect('dashboard:product_list')
    else:
        form = ProductForm()

    return render(request, 'dashboard/product_form.html', {
        'form': form,
        'is_edit': False,
        'title': 'Add New Herbal Product'
    })


@staff_member_required(login_url='dashboard:login')
def dashboard_product_edit_view(request, pk):
    """
    Edit product view (Section 6.4):
    Pre-populated form with live image preview.
    """
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Product '{product.name}' was updated successfully!")
            return redirect('dashboard:product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'dashboard/product_form.html', {
        'form': form,
        'product': product,
        'is_edit': True,
        'title': f'Edit Formulation: {product.name}'
    })


@staff_member_required(login_url='dashboard:login')
def dashboard_product_delete_view(request, pk):
    """
    Delete product view (Section 6.4):
    Requires explicit confirmation step before removing from database.
    """
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f"Product '{product_name}' has been safely deleted.")
        return redirect('dashboard:product_list')

    return render(request, 'dashboard/product_confirm_delete.html', {'product': product})


@staff_member_required(login_url='dashboard:login')
def dashboard_enquiry_list_view(request):
    """
    Enquiries / Orders management view (Section 6.5):
    Lists customer enquiries, supports status updating and status/search filtering.
    """
    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()

    enquiries = Enquiry.objects.select_related('product').all().order_by('-created_at')

    if query:
        enquiries = enquiries.filter(
            Q(name__icontains=query) | 
            Q(phone_number__icontains=query) | 
            Q(message__icontains=query) |
            Q(product__name__icontains=query)
        )

    if status_filter:
        enquiries = enquiries.filter(status=status_filter)

    context = {
        'enquiries': enquiries,
        'query': query,
        'status_filter': status_filter,
        'status_choices': Enquiry.STATUS_CHOICES,
        'total_count': Enquiry.objects.count(),
        'new_count': Enquiry.objects.filter(status='new').count(),
    }
    return render(request, 'dashboard/enquiry_list.html', context)


@staff_member_required(login_url='dashboard:login')
def dashboard_enquiry_status_update_view(request, pk):
    """
    Quick status transition handler (Section 6.5).
    """
    enquiry = get_object_or_404(Enquiry, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Enquiry.STATUS_CHOICES):
            enquiry.status = new_status
            if new_status == 'resolved':
                enquiry.is_processed = True
            elif new_status == 'new':
                enquiry.is_processed = False
            enquiry.save()
            messages.success(request, f"Enquiry #{enquiry.id} from {enquiry.name} marked as '{enquiry.get_status_display()}'.")
        else:
            messages.error(request, "Invalid status choice.")

    return redirect(request.META.get('HTTP_REFERER') or 'dashboard:enquiry_list')


@staff_member_required(login_url='dashboard:login')
def dashboard_enquiry_delete_view(request, pk):
    """
    Deletes customer enquiry.
    """
    enquiry = get_object_or_404(Enquiry, pk=pk)
    if request.method == 'POST':
        name = enquiry.name
        enquiry.delete()
        messages.success(request, f"Enquiry from '{name}' removed.")
    return redirect('dashboard:enquiry_list')
