from django.shortcuts import render , redirect
from scomp.models import TimeSlotModel , UserRegistrationModel , CustomerFormModel , NotificationModel , ServiceModel , SubServiceModel , PackageModel ,PackageTypeModel
from scomp.models import AdvantageModel , WorkModel , WorkImageModel , TimeSlotModel ,TermModel ,OfferModel , BlogModel , BlogParaModel
from UserApp.models import  UserPersonalData , UserAddressModel
from ProfessionalApp.models import ProfessionalDataModel
from UserApp.models import OrderModel

from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home(request):
    obj = OrderModel.objects.filter(status = "Order success",profid="").order_by('-orderdate')
    return render(request,'AdminAppTemp/adminhome.html',{'obj':obj})

@login_required
def serveprof(request,id):
    ordobj = OrderModel.objects.get(id=id)
    prfobj = ProfessionalDataModel.objects.filter(subservice = ordobj.package.subservice)
    lis = {}
    for i in prfobj:
        userreg = UserRegistrationModel.objects.get(user__username = i.userreg.user.username)
        lis[UserPersonalData.objects.get(userreg=userreg)] = UserAddressModel.objects.get(userreg=userreg)

    if request.method == "POST":
        sel = request.POST['seleprof']
        spfobj = OrderModel.objects.filter(id=id)
        if sel == "Null":
            spfobj.update(profid = "Null")
        else:
            userregobj = UserRegistrationModel.objects.get(id = sel)
            profid = ProfessionalDataModel.objects.get(userreg = userregobj).profid
            spfobj.update(profid = profid)
        return redirect('/AdminApp/home/')

    return render(request,'AdminAppTemp/serveprof.html',{'ord':ordobj,'lis':lis})

@login_required
def customerresp(request):
    obj = CustomerFormModel.objects.all()
    return render(request,'AdminAppTemp/customerresp.html',{'obj':obj})

@login_required
def completed(request):
    obj = OrderModel.objects.filter(status = "Completed").order_by('-orderdate')
    return render(request,'AdminAppTemp/history.html',{'obj':obj})

@login_required
def orderslist(request):
    obj = OrderModel.objects.filter(status = "Order success").order_by('-orderdate')
    return render(request,'AdminAppTemp/orderslist.html',{'obj':obj})

@login_required
def notifications(request):
    nobj = NotificationModel.objects.all().order_by('-ndate')
    if request.method == "POST":
        users = request.POST['wnselect']
        sub = request.POST['wnsub']
        tarea = request.POST['wntarea']
        if users == "Users" or users == "Professionals":
            obj = NotificationModel(ntype = users,subject=sub,content=tarea)
            obj.save()
    return render(request,'AdminAppTemp/notifications.html',{'nobj':nobj})

@login_required
def delnotification(request,id):
    obj = NotificationModel.objects.get(id = id)
    obj.delete()
    return redirect('/AdminApp/notifications/')

@login_required
def create(request):
    return render(request,'AdminAppTemp/create.html')

@login_required
def createservices(request):
    obj = ServiceModel.objects.all()
    count = len(obj)
    if request.method == "POST":
        try:
            if request.POST['addservicebutton'] == "addservicebutton":
                newname = request.POST['newservicename']
                serdesc = request.POST['servicedesc']
                obj = ServiceModel(name = newname,desc = serdesc)
                obj.save()
        except Exception as e:
            print(e)
        try:
            if request.POST['deleteservicebutton'] == "deleteservicebutton":
                delid = request.POST['deleteserviceselect']
                obj = ServiceModel.objects.filter(id = delid)
                obj.delete()
        except Exception as e:
            print(e)
        try:
            if request.POST['updateservicebutton'] == "updateservicebutton":
                serid = request.POST['updateservice']
                serup = request.POST['updatedname']
                serdesc = request.POST['servicedesc']
                serobj = ServiceModel.objects.filter(id = serid)
                serobj.update(name = serup,desc = serdesc)
        except Exception as e:
            print(e)
        return redirect("/AdminApp/createservices/")
    return render(request,'AdminAppTemp/createservices.html',{'obj':obj,'count':count})

@login_required
def createsubservices(request):
    obj = SubServiceModel.objects.all()
    count = len(obj)
    if request.method == "POST":
        try:
            if request.POST['addservicebutton'] == "addservicebutton":
                newname = request.POST['newservicename']
                obj = SubServiceModel(name = newname)
                obj.save()
        except Exception as e:
            print(e)
        try:
            if request.POST['deleteservicebutton'] == "deleteservicebutton":
                delid = request.POST['deleteserviceselect']
                obj = SubServiceModel.objects.filter(id = delid)
                obj.delete()
        except Exception as e:
            print(e)
        try:
            if request.POST['updateservicebutton'] == "updateservicebutton":
                serid = request.POST['updateservice']
                serup = request.POST['updatedname']
                serobj = SubServiceModel.objects.filter(id = serid)
                serobj.update(name = serup)
        except Exception as e:
            print(e)
        return redirect("/AdminApp/createsubservices/")
    return render(request,'AdminAppTemp/createsubservices.html',{'obj':obj,'count':count})

@login_required
def createpackages(request):
    obj = PackageModel.objects.all()
    count = len(obj)
    sm = ServiceModel.objects.all()
    ssm = SubServiceModel.objects.all()
    ptype = PackageTypeModel.objects.all()
    offobj = OfferModel.objects.all()
    if request.method == "POST":
        try:
            name= request.POST['packname']
            img= request.FILES['packimg']
            packtypeid= request.POST['packtype']
            serrviceid= request.POST['packservice']
            subserviceid= request.POST['packsubservice']
            details= request.POST['packdetails']
            price= request.POST['packprice']
            offerprice= request.POST['packofferprice']
            offernameid= request.POST['packoffer'].split()[0]
            packtype = PackageTypeModel.objects.get(id = packtypeid)
            service = ServiceModel.objects.get(id = serrviceid)
            subservice = SubServiceModel.objects.get(id = subserviceid)
            offername = OfferModel.objects.get(id = offernameid)
            packobj = PackageModel(name=name,image=img,packagetype=packtype,service=service,subservice=subservice,details=details,price=price,offerprice=offerprice,offername=offername)
            packobj.save()
        except Exception as e:
            print(e)
        return redirect("/AdminApp/createpackages/")
    return render(request,'AdminAppTemp/createpackages.html',{'obj':obj,'count':count,'sm':sm,'ssm':ssm,'ptype':ptype,'offobj':offobj})

@login_required
def packagedetails(request,id):
    obj = PackageModel.objects.get(id = id)
    sm = ServiceModel.objects.all()
    ssm = SubServiceModel.objects.all()
    ptype = PackageTypeModel.objects.all()
    offobj = OfferModel.objects.all()
    if request.method == "POST":
        try:
            name= request.POST['packname']
            # img= request.FILES['packimg']
            packtypeid= request.POST['packtype']
            serrviceid= request.POST['packservice']
            subserviceid= request.POST['packsubservice']
            details= request.POST['packdetails']
            price= request.POST['packprice']
            offerprice= request.POST['packofferprice']
            offernameid= request.POST['packoffer'].split()[0]
            packtype = PackageTypeModel.objects.get(id = packtypeid)
            service = ServiceModel.objects.get(id = serrviceid)
            subservice = SubServiceModel.objects.get(id = subserviceid)
            offername = OfferModel.objects.get(id = offernameid)
            packobj = PackageModel.objects.filter(id = id)
            packobj.update(name=name,packagetype=packtype,service=service,subservice=subservice,details=details,price=price,offerprice=offerprice,offername=offername)
        except Exception as e:
            print(e)
        return redirect("/AdminApp/packagedetails/{}/".format(id))
    return render(request,'AdminAppTemp/adminpackagedetails.html',{'obj':obj,'sm':sm,'ssm':ssm,'ptype':ptype,'offobj':offobj,'id':id})

@login_required
def createoffers(request):
    obj = OfferModel.objects.all()
    count = len(obj)
    if request.method == "POST":
        try:
            if request.POST['addservicebutton'] == "addservicebutton":
                newname = request.POST['newofferename']
                offer = request.POST['newofferper']
                obj = OfferModel(name = newname,offer=offer)
                obj.save()
        except Exception as e:
            print(e)
        try:
            if request.POST['deleteservicebutton'] == "deleteservicebutton":
                delid = request.POST['deleteserviceselect']
                obj = OfferModel.objects.filter(id = delid)
                obj.delete()
        except Exception as e:
            print(e)
        try:
            if request.POST['updateservicebutton'] == "updateservicebutton":
                serid = request.POST['updateservice']
                serup = request.POST['updatedname']
                offer = request.POST['updatedqty']
                serobj = OfferModel.objects.filter(id = serid)
                serobj.update(name = serup,offer=offer)
        except Exception as e:
            print(e)
        return redirect("/AdminApp/createoffers/")
    return render(request,'AdminAppTemp/createoffers.html',{'obj':obj,'count':count})

@login_required
def createterms(request):
    obj = TermModel.objects.all()
    count = len(obj)
    if request.method == "POST":
        try:
            if request.POST['addservicebutton'] == "addservicebutton":
                newname = request.POST['newofferename']
                obj = TermModel(term = newname)
                obj.save()
        except Exception as e:
            print(e)
        try:
            if request.POST['deleteservicebutton'] == "deleteservicebutton":
                delid = request.POST['deleteserviceselect']
                obj = TermModel.objects.filter(id = delid)
                obj.delete()
        except Exception as e:
            print(e)
        try:
            if request.POST['updateservicebutton'] == "updateservicebutton":
                serid = request.POST['updateservice']
                serup = request.POST['updatedname']
                serobj = TermModel.objects.filter(id = serid)
                serobj.update(term = serup)
        except Exception as e:
            print(e)
        return redirect("/AdminApp/createterms/")
    return render(request,'AdminAppTemp/createterms.html',{'obj':obj,'count':count})

@login_required
def createadvantages(request):
    obj = AdvantageModel.objects.all()
    count = len(obj)
    if request.method == "POST":
        try:
            if request.POST['addservicebutton'] == "addservicebutton":
                newname = request.POST['newofferename']
                obj = AdvantageModel(advantage = newname)
                obj.save()
        except Exception as e:
            print(e)
        try:
            if request.POST['deleteservicebutton'] == "deleteservicebutton":
                delid = request.POST['deleteserviceselect']
                obj = AdvantageModel.objects.filter(id = delid)
                obj.delete()
        except Exception as e:
            print(e)
        try:
            if request.POST['updateservicebutton'] == "updateservicebutton":
                serid = request.POST['updateservice']
                serup = request.POST['updatedname']
                serobj = AdvantageModel.objects.filter(id = serid)
                serobj.update(advantage = serup)
        except Exception as e:
            print(e)
        return redirect("/AdminApp/createadvantages/")
    return render(request,'AdminAppTemp/createadvantages.html',{'obj':obj,'count':count})

@login_required
def createworkselectors(request):
    obj = WorkModel.objects.all()
    count = len(obj)
    if request.method == "POST":
        try:
            if request.POST['addservicebutton'] == "addservicebutton":
                newname = request.POST['newofferename']
                offer = request.POST['newofferper']
                obj = WorkModel(name = newname,dataselector=offer)
                obj.save()
        except Exception as e:
            print(e)
        try:
            if request.POST['deleteservicebutton'] == "deleteservicebutton":
                delid = request.POST['deleteserviceselect']
                obj = WorkModel.objects.filter(id = delid)
                obj.delete()
        except Exception as e:
            print(e)
        try:
            if request.POST['updateservicebutton'] == "updateservicebutton":
                serid = request.POST['updateservice']
                serup = request.POST['updatedname']
                offer = request.POST['updatedqty']
                serobj = WorkModel.objects.filter(id = serid)
                serobj.update(name = serup,dataselector=offer)
        except Exception as e:
            print(e)
        return redirect("/AdminApp/createworkselectors/")
    return render(request,'AdminAppTemp/createworkselectors.html',{'obj':obj,'count':count})

@login_required
def createworkimages(request):
    obj = WorkImageModel.objects.all()
    wobj = WorkModel.objects.all()
    count = len(obj)
    if request.method == "POST":
        try:
            if request.POST['addwork'] == "addwork":
                worknameid = request.POST['workname']
                wgobj = WorkModel.objects.get(id = worknameid)
                workimg = request.FILES['workimg']
                obj = WorkImageModel(workselector = wgobj,image = workimg)
                obj.save()
        except Exception as e:
            print(e)
        try:
            if request.POST['workbutton'] == "workbutton":
                workimgid = request.POST['workimgid']
                wiobj = WorkImageModel.objects.get(id = workimgid)
                wiobj.delete()
        except Exception as e:
            print(e)
        return redirect("/AdminApp/createworkimages/")
    return render(request,'AdminAppTemp/createworkimages.html',{'obj':obj,'count':count,'wobj':wobj})

@login_required
def createtimeslots(request):
    obj = TimeSlotModel.objects.all()
    count = len(obj)
    if request.method == "POST":
        try:
            if request.POST['addservicebutton'] == "addservicebutton":
                newname = request.POST['newofferename']
                obj = TimeSlotModel(slot = newname)
                obj.save()
        except Exception as e:
            print(e)
        try:
            if request.POST['deleteservicebutton'] == "deleteservicebutton":
                delid = request.POST['deleteserviceselect']
                obj = TimeSlotModel.objects.filter(id = delid)
                obj.delete()
        except Exception as e:
            print(e)
        try:
            if request.POST['updateservicebutton'] == "updateservicebutton":
                serid = request.POST['updateservice']
                serup = request.POST['updatedname']
                serobj = TimeSlotModel.objects.filter(id = serid)
                serobj.update(slot = serup)
        except Exception as e:
            print(e)
        return redirect("/AdminApp/createtimeslots/")
    return render(request,'AdminAppTemp/createtimeslots.html',{'obj':obj,'count':count})

@login_required
def createblog(request):
    obj = BlogModel.objects.all()
    count = len(obj)
    return render(request,'AdminAppTemp/createblog.html',{'obj':obj,'count':count})

@login_required
def createblogpara(request):
    obj = BlogParaModel.objects.all()
    count = len(obj)
    return render(request,'AdminAppTemp/createblogpara.html',{'obj':obj,'count':count})
