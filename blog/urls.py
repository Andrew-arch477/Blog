from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.Login_View.as_view(), name='login_page'),
    path('logout/', views.Logout_View.as_view(), name='logout_page'),
    path('registration/', views.Registration_View.as_view(), name='registration_page'),
]