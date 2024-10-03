from django.contrib import admin
from django.urls import path, include
from Home import views

urlpatterns = [
    path("TnPStats", views.TnPStats, name="Stats"),
    path("login", views.login, name="login"),
    path("internshipStats", views.internship, name="internship"),
    path("placementStats", views.placement, name="placements"),
    path('studentdashboard',views.student, name='studentdashboard'),
]
