from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from depth_of_field_calc import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/calculate-dof/', views.calculate_dof, name='calculate_dof'),
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    
]