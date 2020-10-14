from django.shortcuts import render , redirect

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from uuid import uuid4

from .models import UserRegistrationModel , ServiceModel , WorkImageModel , WorkModel , CustomerFormModel , PackageModel , BlogModel , BlogParaModel
from UserApp.models import UserAddressModel , UserPersonalData

from ProfessionalApp.models import ProfessionalDataModel , ProfessionalRatingModel


def home(request):
    obj = ServiceModel.objects.all()[:5]
    wobj = WorkModel.objects.all()
    wiobj = WorkImageModel.objects.all()
    uobj = UserRegistrationModel.objects.all()
    blog = BlogModel.objects.filter().order_by('-date')[:3]

    if request.method == 'POST':
        first = request.POST['firstname']
        last = request.POST['lastname']
        email = request.POST['emailid']
        message = request.POST['comp']
        subject = request.POST['subject']
        csobj = CustomerFormModel(first=first,last=last,email=email,subject=subject,message=message)
        csobj.save()
        return render(request,'index.html',{'obj':obj,'wobj':wobj,'wiobj':wiobj,'message':'Response have been saved'})

    return render(request,'index.html',{'obj':obj,'wobj':wobj,'wiobj':wiobj,'message':'','blog':blog})

def selectBooking(request):
    shobj = ServiceModel.objects.all()
    sprod = ''
    if request.method == "POST":
        sprod = PackageModel.objects.all()
        lis = request.POST['sdata'].split(' ')
        nlis=set()
        for i in lis:
            for j in sprod:
                if i.lower() in j.name.lower():
                    print(j.name)
                    nlis.add(j)
        message=""
        if not nlis:
            message = "No result found"
        else:
            message = "Search results"
        return render(request,'selectBooking.html',{'sprod':nlis,'message':message})
    shdic = {}
    for i in shobj:
        serve = ServiceModel.objects.get(id = i.id)
        shdic[i]=PackageModel.objects.filter(service = serve)
    return render(request,'selectBooking.html',{'shdic':shdic,'sprod':sprod})

def blogPage(request,id):
    blog = BlogModel.objects.get(id = id)
    blogpara = BlogParaModel.objects.filter(blog = blog)
    return render(request,'single.html',{'blog':blog,'blogpara':blogpara})

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        selecteduser = authenticate(username = username,password = password)
        if selecteduser:
            if selecteduser.is_active:
                login(request,selecteduser)
                udata = UserRegistrationModel.objects.get(user__username=request.user)
                if udata.usertype == 'User':
                    return redirect('/UserApp/home/')
                elif udata.usertype == 'Admin':
                    return redirect('/AdminApp/home/')
                elif udata.usertype == 'Professional':
                    return redirect('/ProfessionalApp/home/')
                else:
                    return redirect('/')
            else:
                return HttpResponse("<h1>User deactivated</h1>")
        else:
            return render(request,'signin.html',{'filler':'Alert : Email or Password does not match please try again'})
    else:
        return render(request,'signin.html')

def getprofid():
    obj = ProfessionalDataModel.objects.all()
    lis=[]
    for i in obj:
        lis.append(i.profid)
    while(True):
        strid = str(uuid4())
        if strid in lis:
            pass
        else:
            return strid

def signup(request):
    if request.method == 'POST':
        mobile = request.POST['mobile']
        username = request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        usertype = request.POST['usertype']

        getallobj = UserRegistrationModel.objects.all()
        for i in  getallobj:
            if i.mobile == mobile:
                return render(request,'signup.html',{'message':"This Mobile number is already registered"})

        for i in getallobj:
            if i.user.username == username:
                return render(request,'signup.html',{'message':"This Mail Id is already registered"})

        uobj = User(username=username)
        uobj.save()
        uobj.set_password(password)
        uobj.save()
        upobj = UserRegistrationModel(user=uobj,mobile=mobile,usertype=usertype)
        upobj.save()

        userpobj = UserPersonalData(userreg=upobj,name="",aadhar="")
        userpobj.save()

        useradd = UserAddressModel(userreg=upobj,flat="",street="",landmark="",area="",city="",district="",pin="",state="")
        useradd.save()

        selecteduser = authenticate(username = username,password = password)
        if selecteduser:
            if selecteduser.is_active:
                login(request,selecteduser)
                udata = UserRegistrationModel.objects.get(user__username=request.user)
                if udata.usertype == 'User':
                    return redirect('/UserApp/home/')
                elif udata.usertype == 'Admin':
                    return redirect('/AdminApp/home/')
                elif udata.usertype == 'Professional':
                    pid = getprofid()
                    profobj = ProfessionalDataModel(userreg=upobj,profid=pid,service=None,subservice=None)
                    profobj.save()

                    prmobj = ProfessionalRatingModel(userreg=upobj,one=0,two=0,three=0,four=0,five=0,total=0,avrage=0.0)
                    prmobj.save()

                    return redirect('/ProfessionalApp/home/')
                else:
                    return redirect('/SignIn/')
            else:
                return HttpResponse("<h1>User deactivated</h1>")
        else:
            return redirect('/SignIn/')

    return render(request,'signup.html',{'message':'Hurray! Going for Signing Up'})

@login_required
def signout(request):
    logout(request)
    return redirect('/')


def adminsignup(request):
    if request.method == 'POST':
        mobile = request.POST['mobile']
        username = request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        usertype = request.POST['usertype']

        getallobj = UserRegistrationModel.objects.all()
        for i in  getallobj:
            if i.mobile == mobile:
                return render(request,'adminsignup.html',{'message':"This Mobile number is already registered"})

        for i in getallobj:
            if i.user.username == username:
                return render(request,'adminsignup.html',{'message':"This Mail Id is already registered"})

        uobj = User(username=username)
        uobj.save()
        uobj.set_password(password)
        uobj.save()
        upobj = UserRegistrationModel(user=uobj,mobile=mobile,usertype=usertype)
        upobj.save()

        selecteduser = authenticate(username = username,password = password)
        if selecteduser:
            if selecteduser.is_active:
                login(request,selecteduser)
                udata = UserRegistrationModel.objects.get(user__username=request.user)
                if udata.usertype == 'User':
                    return redirect('/UserApp/home/')
                elif udata.usertype == 'Admin':
                    print("admin called")
                    return redirect('/AdminApp/home/')
                elif udata.usertype == 'Professional':
                    return redirect('/ProfessionalApp/home/')
                else:
                    return redirect('/SignIn/')
            else:
                return HttpResponse("<h1>User deactivated</h1>")
        else:
            return redirect('/SignIn/')
    return render(request,'adminsignup.html',{'message':'Hurray! Going for Signing Up'})
