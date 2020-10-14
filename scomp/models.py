from django.db import models
from django.contrib.auth.models import User

class UserRegistrationModel(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10)
    usertype = models.CharField(max_length=15)
    def __str__(self):
        return self.mobile

class ServiceModel(models.Model):
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=200,default='')
    def __str__(self):
        return self.name

class SubServiceModel(models.Model):
    name = models.CharField(max_length=50)
    service = models.ForeignKey(ServiceModel,on_delete=models.PROTECT,null=True)
    def __str__(self):
        return self.name

class WorkModel(models.Model):
    name = models.CharField(max_length=50)
    dataselector = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class WorkImageModel(models.Model):
    workselector = models.ForeignKey(WorkModel,on_delete=models.PROTECT)
    image = models.FileField(upload_to='workImagesFolder',blank=True, null=True)
    def __str__(self):
        return self.image.url

class CustomerFormModel(models.Model):
    first = models.CharField(max_length=30)
    last = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    subject = models.CharField(max_length=30)
    message = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.email

class AdvantageModel(models.Model):
    advantage = models.CharField(max_length=100)
    def __str__(self):
        return self.advantage

class TermModel(models.Model):
    term = models.CharField(max_length=300)
    def __str__(self):
        return self.term

class PackageTypeModel(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class OfferModel(models.Model):
    name = models.CharField(max_length=60)
    offer = models.IntegerField()
    def __str__(self):
        return self.name+" ,"+str(self.offer)+"% OFF"

class PackageModel(models.Model):
    name = models.CharField(max_length=60)
    image = models.FileField(upload_to='packageImagesFolder',blank=True, null=True)
    packagetype = models.ForeignKey(PackageTypeModel,on_delete=models.PROTECT)
    service = models.ForeignKey(ServiceModel,on_delete=models.PROTECT)
    subservice = models.ForeignKey(SubServiceModel,on_delete=models.PROTECT)
    details = models.CharField(max_length=200)
    price = models.IntegerField()
    offerprice = models.IntegerField()
    offername = models.ForeignKey(OfferModel,on_delete=models.PROTECT,null=True)
    def __str__(self):
        return self.name

class TimeSlotModel(models.Model):
    slot = models.CharField(max_length=20)
    def __str__(self):
        return self.slot

class NotificationModel(models.Model):
    ntype = models.CharField(max_length=15)
    subject = models.CharField(max_length=200)
    content = models.CharField(max_length=1000)
    ndate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject+" "+str(self.ndate)

class BlogModel(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to='blogimages',blank=True, null=True)
    blogauthor = models.CharField(max_length=30)
    aboutauthor = models.CharField(max_length=200)
    intropara = models.CharField(max_length=150)
    content = models.CharField(max_length=500)

    def __str__(self):
        return self.title

class BlogParaModel(models.Model):
    blog = models.ForeignKey(BlogModel,on_delete=models.CASCADE)
    title = models.CharField(max_length = 100)
    image = models.FileField(upload_to='blogimages',blank=True, null=True)
    content = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title+" ("+str(self.blog)+")"
