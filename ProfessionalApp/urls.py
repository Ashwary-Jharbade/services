from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home),
    path('profile/',views.profile),
    path('editprofile/',views.editprofile),
    path('history/',views.history),
    path('ordersuccess/<int:id>/',views.ordersuccess),
    path('notification/',views.notification),
]
