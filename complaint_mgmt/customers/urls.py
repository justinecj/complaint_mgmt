from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
    path('add/', views.customer_create, name='customer_create'),
    path('edit/<int:pk>/', views.customer_edit, name='customer_edit'),
]
