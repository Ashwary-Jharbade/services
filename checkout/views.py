from django.shortcuts import render , redirect
from django.http import HttpResponse

from uuid import uuid4
import time
from UserApp.models import OrderModel , UserRegistrationModel , TimeSlotModel , PackageModel

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Import Payu from Paywix
from paywix.payu import Payu
import time

payu_config = settings.PAYU_CONFIG
merchant_key = payu_config.get('merchant_key')
merchant_salt = payu_config.get('merchant_salt')
surl = payu_config.get('success_url')
furl = payu_config.get('failure_url')
mode = payu_config.get('mode')

# Create Payu Object for making transaction
# The given arguments are mandatory
payu = Payu(merchant_key, merchant_salt, surl, furl, mode)


def getorderid():
    oid = OrderModel.objects.all()
    lis = []
    for i in oid:
        lis.append(i.orderid)
    while(True):
        strid = str(uuid4())
        if strid in lis:
            pass
        else:
            return strid

# Payu checkout page

globeorderid = ''

@csrf_exempt
@login_required
def payu_checkout(request):
    if request.method == 'POST':
        orderid = getorderid()
        global globeorderid
        globeorderid = orderid
        userreg = UserRegistrationModel.objects.get(user__username = request.user.username)
        profid = ''
        name = request.POST['vname']
        mobile = request.POST['vmob']
        email = request.POST['vemail']
        address = request.POST['vaddress']
        date = request.POST['vdate']
        timeslotid = request.POST['vtime']
        timeslot = TimeSlotModel.objects.get(id = timeslotid)
        amount = request.POST['totalamountn']
        paymode = "Online"
        status ="Ordered"

        packageid = request.POST.getlist('packid')
        qty = request.POST.getlist('vqty')

        checkamt = 0
        objlist = []
        for i in range(len(qty)):
            package = PackageModel.objects.get(id = packageid[i])
            qtys=qty[i]
            amt = int(qtys) * int(package.offerprice)
            checkamt = checkamt + amt
            objlist.append(OrderModel(userreg=userreg,orderid=orderid,profid=profid,name=name,mobile=mobile,email=email,address=address,date=date,timeslot=timeslot,package=package,qty=qtys,amount=amt,paymode=paymode,status=status))

        if checkamt < 500:
            checkamt = checkamt+50

        if checkamt == int(amount):
            for i in objlist:
                i.save()
        else:
            return HttpResponse("Amount doesn't matchup something wrong with browser please change browser")

        # Making Checkout form into dictionary
        # data = {k: v[0] for k, v in dict(request.POST).items()}
        # data.pop('csrfmiddlewaretoken')
        # The dictionary data  should be contains following details
        data = { 'amount': amount,
            'firstname': name,
            'email': email,
            'phone': mobile, 'productinfo': "Usync Package",
            'lastname': 'test', 'address1': address,
            'address2': '', 'city': '',
            'state': '', 'country': '',
            'zipcode': '', 'udf1': '',
            'udf2': '', 'udf3': '', 'udf4': '', 'udf5': ''
        }

        # No Transactio ID's, Create new with paywix, it's not mandatory
        # Create your own
        # Create transaction Id with payu and verify with table it's not existed
        txnid = orderid
        data.update({"txnid": txnid})
        payu_data = payu.transaction(**data)
        #return render(request, 'payu_checkout.html', {"posted": payu_data})
        return redirect('/Checkout/success/')

@csrf_exempt
def success(request):
    data = {k: v[0] for k, v in dict(request.POST).items()}
    response = payu.verify_transaction(data)
    sobj = OrderModel.objects.filter(orderid = globeorderid)
    sobj.update(status="Order success")
    return render(request,'success.html')

@csrf_exempt
def failure(request):
    data = {k: v[0] for k, v in dict(request.POST).items()}
    response = payu.verify_transaction(data)
    sobj = OrderModel.objects.filter(orderid = globeorderid)
    sobj.update(status="Order failed")
    return render(request,'failure.html')
