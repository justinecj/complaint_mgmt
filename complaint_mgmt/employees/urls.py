from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('add/', views.employee_create, name='employee_create'),
    path('edit/<int:pk>/', views.employee_edit, name='employee_edit'),
    path('detail/<int:pk>/', views.employee_detail, name='employee_detail'),
]
