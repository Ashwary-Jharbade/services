from django.shortcuts import render , redirect
from scomp.models import UserRegistrationModel , ServiceModel , SubServiceModel , NotificationModel
from UserApp.models import UserAddressModel , UserPersonalData , OrderModel
from .models import ProfessionalDataModel , ProfessionalRatingModel

from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    userreg = UserRegistrationModel.objects.get(user__username = request.user.username)
    prm = ProfessionalRatingModel.objects.get(userreg = userreg)
    prfdm = ProfessionalDataModel.objects.get(userreg = userreg)
    ord = OrderModel.objects.filter(profid = prfdm.profid,status="Order success").order_by('-orderdate')
    return render(request,'ProfessionalAppTemp/professionalhome.html',{'prm':prm,'ord':ord})

@login_required
def profile(request):
    userreg = UserRegistrationModel.objects.get(user__username = request.user.username)
    udobj = UserPersonalData.objects.get(userreg = userreg)
    adobj = UserAddressModel.objects.get(userreg = userreg)
    probj = ProfessionalDataModel.objects.get(userreg = userreg)
    return render(request,'ProfessionalAppTemp/profile.html',{'udobj':udobj,'userreg':userreg,'adobj':adobj,'probj':probj})

@login_required
def editprofile(request):
    userreg = UserRegistrationModel.objects.get(user__username = request.user.username)
    udobj = UserPersonalData.objects.get(userreg = userreg)
    adobj = UserAddressModel.objects.get(userreg = userreg)
    uservice = ServiceModel.objects.all()
    usub = SubServiceModel.objects.all()
    userobj = UserPersonalData.objects.filter(userreg = userreg)
    addressobj = UserAddressModel.objects.filter(userreg = userreg)
    probj = ProfessionalDataModel.objects.filter(userreg = userreg)
    if request.method == "POST":
        name = request.POST['uname']
        aadhar = request.POST['aadhar']
        flat = request.POST['flat']
        street = request.POST['line']
        landmark = request.POST['landmark']
        city = request.POST['city']
        district = request.POST['district']
        pin = request.POST['pin']
        state = request.POST['state']
        sub = request.POST['subservice']
        if sub=="None":
            probj.update(service=None,subservice=None)
        else:
            ssm = SubServiceModel.objects.get(id=sub)
            sm = ServiceModel.objects.get(id = ssm.service.id)
            probj.update(service=sm,subservice=ssm)
        userobj.update(name=name,aadhar=aadhar)
        addressobj.update(flat=flat,street=street,landmark=landmark,city=city,district=district,pin=pin,state=state)
        return redirect('/ProfessionalApp/profile/')
    return render(request,'ProfessionalAppTemp/editprofile.html',{'udobj':udobj,'adobj':adobj,'usub':usub,'probj':probj})

@login_required
def history(request):
    userreg = UserRegistrationModel.objects.get(user__username = request.user.username)
    profdata = ProfessionalDataModel.objects.get(userreg = userreg)
    ordmod = OrderModel.objects.filter(profid = profdata.profid,status="Completed").order_by('-orderdate')
    return render(request,'ProfessionalAppTemp/history.html',{'ordmod':ordmod})

@login_required
def ordersuccess(request,id):
    ordmod = OrderModel.objects.get(id = id)
    userreg = UserRegistrationModel.objects.get(user__username = request.user.username)
    profdata = ProfessionalDataModel.objects.get(userreg = userreg)
    if(ordmod.profid == profdata.profid):
        ordq = OrderModel.objects.filter(id = id)
        ordq.update(status = "Completed")
    else:
        print('Not authorised')
    return redirect('/ProfessionalApp/home/')

@login_required
def notification(request):
    obj = NotificationModel.objects.filter(ntype = "Professionals").order_by('-ndate')
    return render(request,'ProfessionalAppTemp/notification.html',{'obj':obj})
