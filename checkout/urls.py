from django.urls import path
from .import views
urlpatterns = [
    path('home/',views.payu_checkout),
    path('success/',views.success),
    path('failure/',views.failure),
]
