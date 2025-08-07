from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.Main_Page_View.as_view(), name='main_page'),

    path('login/', views.Login_View.as_view(), name='login_page'),
    path('logout/', views.Logout_View.as_view(), name='logout_page'),
    path('registration/', views.Registration_View.as_view(), name='registration_page'),
    path('profile/', views.Profile_View.as_view(), name='profile_page'),
]