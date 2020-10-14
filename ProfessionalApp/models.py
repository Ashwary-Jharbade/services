from django.db import models
from scomp.models import ServiceModel , SubServiceModel , UserRegistrationModel
# Create your models here.

class ProfessionalDataModel(models.Model):
    userreg = models.ForeignKey(UserRegistrationModel,on_delete=models.CASCADE)
    profid = models.CharField(max_length=36)
    service = models.ForeignKey(ServiceModel,on_delete=models.CASCADE,null=True)
    subservice = models.ForeignKey(SubServiceModel,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return str(self.userreg)+"("+str(self.profid)+")"

class ProfessionalRatingModel(models.Model):
    userreg = models.ForeignKey(UserRegistrationModel,on_delete=models.CASCADE)
    one = models.IntegerField()
    two = models.IntegerField()
    three = models.IntegerField()
    four = models.IntegerField()
    five = models.IntegerField()
    total = models.IntegerField()
    avrage = models.CharField(max_length=3)
    def __str__(self):
        return self.userreg.mobile
