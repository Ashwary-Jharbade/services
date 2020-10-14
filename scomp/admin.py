from django.contrib import admin
from .models import UserRegistrationModel , ServiceModel , WorkImageModel , WorkModel , CustomerFormModel , SubServiceModel
from .models import AdvantageModel , OfferModel , PackageTypeModel , TermModel , PackageModel , TimeSlotModel , NotificationModel , BlogModel , BlogParaModel


admin.site.register(UserRegistrationModel)
admin.site.register(ServiceModel)
admin.site.register(WorkImageModel)
admin.site.register(WorkModel)
admin.site.register(CustomerFormModel)
admin.site.register(SubServiceModel)
admin.site.register(AdvantageModel)
admin.site.register(OfferModel)
admin.site.register(PackageModel)
admin.site.register(TermModel)
admin.site.register(PackageTypeModel)
admin.site.register(TimeSlotModel)
admin.site.register(NotificationModel)
admin.site.register(BlogModel)
admin.site.register(BlogParaModel)
