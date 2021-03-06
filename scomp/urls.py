"""scomp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('super_secure_admin_interface_signup_path/',views.adminsignup),
    path('',views.home),
    path('Services/',views.selectBooking),
    path('SignIn/',views.signin),
    path('SignUp/',views.signup),
    path('SignOut/',views.signout),
    path('Blog/<int:id>/',views.blogPage),
    path('UserApp/',include('UserApp.urls')),
    path('ProfessionalApp/',include('ProfessionalApp.urls')),
    path('AdminApp/',include('AdminApp.urls')),
    path('Checkout/',include('checkout.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
