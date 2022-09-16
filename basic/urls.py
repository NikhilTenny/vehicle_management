from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',views.loginView, name='login_page'),            # Login
    path('home/', views.homeView.as_view()   , name='home_page'),     # Home page
    path('logout/',auth_views.LogoutView.as_view(), name='logout'),     
    path('home/create',views.CreateView.as_view(), name='create'),     # Create a new record in vehicle model
    path('home/<int:pk>',views.VehicleView.as_view(), name='detail'),    # Show a particular record
    path('home/edit/<int:pk>',views.VehicleEditView.as_view(), name='edit'),    # Show a particular record
    path('home/delete/<int:pk>',views.VehicleDeleteView.as_view(), name='delete'),    # Delete a particular record


]
  