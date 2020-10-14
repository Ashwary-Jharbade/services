from django.shortcuts import render , redirect
from scomp.models import ServiceModel , SubServiceModel , PackageModel ,UserRegistrationModel , TimeSlotModel , NotificationModel
from ProfessionalApp.models import ProfessionalDataModel , ProfessionalRatingModel
from .models import CartModel , UserAddressModel , UserPersonalData , OrderModel

from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def home(request):
    shobj = ServiceModel.objects.all()
    userreg = UserRegistrationModel.objects.get(user__username = request.user.username)
    caobj = CartModel.objects.filter(userreg = userreg)
    cartbatch = len(caobj)
    packobj = PackageModel.objects.all()
    return render(request,'UserAppTemp/userhome.html',{'shobj':shobj,'cartbatch':cartbatch,'packobj':packobj})

@login_required
def servicepage(request,id):
    sobj = ServiceModel.objects.get(id=id)
    ssobj = SubServiceModel.objects.filter(service = sobj)

    userreg = UserRegistrationModel.objects.get(user__username = request.user.username)
    caobj = CartModel.objects.filter(userreg = userreg)
    cartbatch = len(caobj)

    pdic = {}
    profobj = ProfessionalDataModel.objects.filter(service = sobj)
    for i in profobj:
        updobj = UserPersonalData.objects.get(userreg = UserRegistrationModel.objects.get(user__username = i.userreg.user.username))
        prmobj=ProfessionalRatingModel.objects.get(userreg = UserRegistrationModel.objects.get(user__username = i.userreg.user.username))
        pdic[updobj]=prmobj
    return render(request,'UserAppTemp/servicedesc.html',{'sobj':sobj,'ssobj':ssobj,'cartbatch':cartbatch,'profobj':pdic})

@login_required
def packagedesc(request,id):
    ssm = SubServiceModel.objects.get(id=id)
    pobj = PackageModel.objects.filter(subservice = ssm)
    obj = []
    aobj = []
    for i in pobj:
        if i.packagetype.name == 'Package':
            obj.append(i)
    for i in pobj:
        if i.packagetype.name == 'Addon':
            aobj.append(i)

    userreg = UserRegistrationModel.objects.get(user__username = request.user.username)
    caobj = CartModel.objects.filter(userreg = userreg)
    cartbatch = len(caobj)
    return render(request,'UserAppTemp/packagedesc.html',{'obj':obj,'aobj':aobj,'cartbatch':cartbatch})

@login_required
def packagedetails(request,id):
    obj = PackageModel.objects.get(id = id)
    userreg = UserRegistrationModel.objects.get(user__username = request.user.username)
    caobj = CartModel.objects.filter(userreg = userreg)
    cartbatch = len(caobj)
    return render(request,'UserAppTemp/packagedetails.html',{'obj':obj,'cartbatch':cartbatch})

@login_required
def cart(request):
    userreg = UserRegistrationModel.objects.get(user__username = request.user.username)
    caobj = CartModel.objects.filter(userreg = userreg)
    total = 0
    for i in caobj:
        total = total + int(i.package.offerprice)
    print(total)
    totalitems = len(caobj)
    cartbatch = len(caobj)
    count=1
    lis={}
    for i in caobj:
        lis[count]=i
        count+=1
    userpdata = UserPersonalData.objects.get(userreg = userreg)
    useradd = UserAddressModel.objects.get(userreg = userreg)
    timeobj = TimeSlotModel.objects.all()
    return render(request,'UserAppTemp/cart.html',{'caobj':caobj,'total':total,'totalitems':totalitems,'cartbatch':cartbatch,'donut':lis,'upd':userpdata,'userreg':userreg,'useradd':useradd,'timeobj':timeobj})

@login_required
def addtocart(request,id):
    userreg = UserRegistrationModel.objects.get(user__username = request.user.username)
    package = PackageModel.objects.get(id = id)

    try:
        cobj = CartModel(userreg=userreg,package=package)
        cobj.save()
    except Exception:
        print("Items exist in cart")

    caobj = CartModel.objects.filter(userreg = userreg)
    return redirect('/UserApp/cart/')

@login_required
def removefromcart(request,id):
    cartobj = CartModel.objects.filter(id=id)
    cartobj.delete()

    userreg = UserRegistrationModel.objects.get(user__username = request.user.username)
    caobj = CartModel.objects.filter(userreg = userreg)
    return redirect('/UserApp/cart/')

@login_required
def history(request):
    userreg = UserRegistrationModel.objects.get(user__username = request.user.username)
    caobj = CartModel.objects.filter(userreg = userreg)
    cartbatch = len(caobj)
    hobj = OrderModel.objects.filter(userreg=userreg).order_by('-orderdate')
    return render(request,'UserAppTemp/history.html',{'cartbatch':cartbatch,'hobj':hobj})

@login_required
def rateservice(request,id):
    userreg = UserRegistrationModel.objects.get(user__username = request.user.username)
    caobj = CartModel.objects.filter(userreg = userreg)
    cartbatch = len(caobj)
    ordobj = OrderModel.objects.get(id = id)
    ordobjq = OrderModel.objects.filter(id = id)
    profobj = ProfessionalDataModel.objects.get(profid = ordobj.profid)
    ratingq = ProfessionalRatingModel.objects.filter(userreg = profobj.userreg)
    ratingo = ProfessionalRatingModel.objects.get(userreg = profobj.userreg)
    if request.method == 'POST':
        count = 0
        val1 = ratingo.one
        val2 = ratingo.two
        val3 = ratingo.three
        val4 = ratingo.four
        val5 = ratingo.five
        for i in request.POST:
            count+=1
        count = count-2
        if count == 1:
            val1+=1
        elif count == 2:
            val2+=1
        elif count == 3:
            val3+=1
        elif count == 4:
            val4+=1
        elif count == 5:
            val5+=1
        totalval = ratingo.total+1
        print(val1,val2,val3,val4,val5,totalval)
        avgval = (1*val1 + 2*val2 + 3*val3 + 4*val4 + 5*val5 )/totalval
        avgval = str(avgval)[:3]
        ratingq.update(one=val1,two=val2,three=val3,four=val4,five=val5,total=totalval,avrage=avgval)
        ordobjq.update(ratingflag=1)
        return redirect("/UserApp/history/")
    return render(request,'UserAppTemp/rateservice.html',{'cartbatch':cartbatch,'id':id})

@login_required
def profile(request):
    userreg = UserRegistrationModel.objects.get(user__username = request.user.username)
    caobj = CartModel.objects.filter(userreg = userreg)
    cartbatch = len(caobj)
    udobj = UserPersonalData.objects.get(userreg = userreg)
    adobj = UserAddressModel.objects.get(userreg = userreg)
    return render(request,'UserAppTemp/profile.html',{'cartbatch':cartbatch,'udobj':udobj,'userreg':userreg,'adobj':adobj})

@login_required
def editprofile(request):
    userreg = UserRegistrationModel.objects.get(user__username = request.user.username)
    caobj = CartModel.objects.filter(userreg = userreg)
    cartbatch = len(caobj)
    udobj = UserPersonalData.objects.get(userreg = userreg)
    adobj = UserAddressModel.objects.get(userreg = userreg)

    userobj = UserPersonalData.objects.filter(userreg = userreg)
    addressobj = UserAddressModel.objects.filter(userreg = userreg)
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

        userobj.update(name=name,aadhar=aadhar)
        addressobj.update(flat=flat,street=street,landmark=landmark,city=city,district=district,pin=pin,state=state)
        return redirect('/UserApp/profile/')
    return render(request,'UserAppTemp/editprofile.html',{'cartbatch':cartbatch,'udobj':udobj,'adobj':adobj})

@login_required
def buysingle(request,id):
    userreg = UserRegistrationModel.objects.get(user__username = request.user.username)
    userpdata = UserPersonalData.objects.get(userreg = userreg)
    caobj = CartModel.objects.filter(userreg = userreg)
    cartbatch = len(caobj)
    packobj = PackageModel.objects.get(id=id)
    useradd = UserAddressModel.objects.get(userreg = userreg)
    timeobj = TimeSlotModel.objects.all()
    return render(request,'UserAppTemp/buysingle.html',{'cartbatch':cartbatch,'packobj':packobj,'userreg':userreg,'upd':userpdata,'useradd':useradd,'timeobj':timeobj})

@login_required
def buycart(request):
    userreg = UserRegistrationModel.objects.get(user__username = request.user.username)
    caobj = CartModel.objects.filter(userreg = userreg)
    cartbatch = len(caobj)
    return render(request,'UserAppTemp/buycart.html',{'cartbatch':cartbatch,'userreg':userreg})

@login_required
def notification(request):
    userreg = UserRegistrationModel.objects.get(user__username = request.user.username)
    caobj = CartModel.objects.filter(userreg = userreg)
    cartbatch = len(caobj)
    obj = NotificationModel.objects.filter(ntype = "Users").order_by('-ndate')
    return render(request,'UserAppTemp/notification.html',{'cartbatch':cartbatch,'obj':obj})
