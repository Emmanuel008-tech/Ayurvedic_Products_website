from django.urls import path
from . import dashboard_views as views

app_name = 'dashboard'

urlpatterns = [
    # Auth
    path('login/', views.dashboard_login_view, name='login'),
    path('logout/', views.dashboard_logout_view, name='logout'),

    # Overview
    path('', views.dashboard_overview_view, name='overview'),

    # Products CRUD
    path('products/', views.dashboard_product_list_view, name='product_list'),
    path('products/add/', views.dashboard_product_add_view, name='product_add'),
    path('products/<int:pk>/edit/', views.dashboard_product_edit_view, name='product_edit'),
    path('products/<int:pk>/delete/', views.dashboard_product_delete_view, name='product_delete'),

    # Enquiries / Orders Management
    path('enquiries/', views.dashboard_enquiry_list_view, name='enquiry_list'),
    path('enquiries/<int:pk>/status/', views.dashboard_enquiry_status_update_view, name='enquiry_status_update'),
    path('enquiries/<int:pk>/delete/', views.dashboard_enquiry_delete_view, name='enquiry_delete'),
]
