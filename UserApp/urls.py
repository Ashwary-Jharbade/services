from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home),
    path('service/<int:id>/',views.servicepage),
    path('package/<int:id>/',views.packagedesc),
    path('details/<int:id>/',views.packagedetails),
    path('cart/',views.cart),
    path('addtocart/<int:id>/',views.addtocart),
    path('removefromcart/<int:id>/',views.removefromcart),
    path('history/',views.history),
    path('profile/',views.profile),
    path('editprofile/',views.editprofile),
    path('buypackage/<int:id>/',views.buysingle),
    path('buyall/',views.buycart),
    path('rateservice/<int:id>/',views.rateservice),
    path('notification/',views.notification),
]
