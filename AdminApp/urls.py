from django.urls import path
from .import views

urlpatterns = [
    path('home/',views.home),
    path('serveprof/<int:id>/',views.serveprof),
    path('customerresp/',views.customerresp),
    path('completed/',views.completed),
    path('orderslist/',views.orderslist),
    path('notifications/',views.notifications),
    path('delnotification/<int:id>/',views.delnotification),
    path('create/',views.create),
    path('createservices/',views.createservices),
    path('createsubservices/',views.createsubservices),
    path('createpackages/',views.createpackages),
    path('packagedetails/<int:id>/',views.packagedetails),
    path('createoffers/',views.createoffers),
    path('createterms/',views.createterms),
    path('createadvantages/',views.createadvantages),
    path('createworkselectors/',views.createworkselectors),
    path('createworkimages/',views.createworkimages),
    path('createtimeslots/',views.createtimeslots),
    path('createblog/',views.createblog),
    path('createblogpara/',views.createblogpara),
]
