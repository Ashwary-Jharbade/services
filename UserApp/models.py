from django.db import models
from scomp.models import PackageModel , UserRegistrationModel , TimeSlotModel

# Create your models here.

class CartModel(models.Model):
    class Meta:
        unique_together = (('package','userreg'),)
    package = models.ForeignKey(PackageModel,on_delete=models.CASCADE)
    userreg = models.ForeignKey(UserRegistrationModel,on_delete=models.CASCADE)

    def __str__(self):
        return self.userreg.user.username

class UserPersonalData(models.Model):
    userreg = models.ForeignKey(UserRegistrationModel,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,null=True)
    aadhar = models.CharField(max_length=12,null=True)
    def __str__(self):
        return self.userreg.mobile

class UserAddressModel(models.Model):
    userreg = models.ForeignKey(UserRegistrationModel,on_delete=models.CASCADE)
    flat = models.CharField(max_length=20,null=True)
    street = models.CharField(max_length=20,null=True)
    landmark = models.CharField(max_length=20,null=True)
    area = models.CharField(max_length=20,null=True)
    city = models.CharField(max_length=20,null=True)
    district = models.CharField(max_length=20,null=True)
    pin = models.CharField(max_length=6,null=True)
    state = models.CharField(max_length=20,null=True)
    def __str__(self):
        return self.userreg.mobile

class OrderModel(models.Model):
    userreg = models.ForeignKey(UserRegistrationModel,on_delete=models.CASCADE)
    orderid = models.CharField(max_length=36)
    profid = models.CharField(max_length=36,null=True)
    orderdate = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)
    email = models.CharField(max_length=60)
    address = models.CharField(max_length=200)
    date = models.CharField(max_length=10)
    timeslot = models.ForeignKey(TimeSlotModel,on_delete=models.CASCADE)
    package = models.ForeignKey(PackageModel,on_delete=models.CASCADE)
    qty = models.IntegerField()
    amount = models.IntegerField()
    paymode = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    ratingflag = models.IntegerField(default=0)

    def __str__(self):
        return "(Mob No = "+str(self.userreg)+") (Package = "+str(self.package)+") (Order id = "+self.orderid+")  (Status = "+self.status+")"
