from django.urls import path
from . import views

urlpatterns = [
    path('', views.complaint_list, name='complaint_list'),
    path('register/', views.register_complaint, name='register_complaint'),
    path('assigned/', views.assigned_complaints, name='assigned_complaints'),
    path('unassigned/', views.unassigned_complaints, name='unassigned_complaints'),  
    path('<int:pk>/', views.complaint_detail, name='complaint_detail'),
    path('edit/<int:pk>/', views.complaint_edit, name='complaint_edit'),
    path('view/<int:pk>/', views.complaint_readonly_detail, name='complaint_readonly_detail'),

]