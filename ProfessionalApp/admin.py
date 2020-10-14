from django.contrib import admin

from .models import ProfessionalDataModel , ProfessionalRatingModel

# Register your models here.
admin.site.register(ProfessionalDataModel)
admin.site.register(ProfessionalRatingModel)
