from django.urls import path
from . import views

app_name = 'backend'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('products/', views.products_view, name='products'),
    path('contact/', views.contact_view, name='contact'),
]
