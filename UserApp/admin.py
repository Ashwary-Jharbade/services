from django.contrib import admin
from .models import CartModel , UserPersonalData , UserAddressModel , OrderModel
# Register your models here.

admin.site.register(CartModel)
admin.site.register(UserAddressModel)
admin.site.register(UserPersonalData)
admin.site.register(OrderModel)
