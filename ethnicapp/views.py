from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages
from django.db.models import Q
from .models import *

# Create your views here.
def index(request):
    return render(request,"index.html")

def reg(request):
    msg = ''
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        try:
            usr = User.objects.create_user(
                username=email, password=password, is_active=1)
            usr.save()
            par = Customer.objects.create(
                name=name, email=email, phone=phone, address=address, user=usr)
            par.save()
            msg = 'Registration Successfull..'
            return render(request, 'reg.html', {"msg": msg})
        except:
            msg = 'Username already registred..'
            return render(request, 'reg.html', {"msg": msg})

    else:
        return render(request, 'reg.html', {"msg": msg})
    return render(request,"reg.html")

    

def login(request):
    msg=""
    if request.POST:
        name=request.POST['name']
        password=request.POST['password']
        auth=authenticate(username=name,password=password)
        if auth is not None:
            if auth.is_superuser:
                return redirect("/adminHome")
            elif auth.is_staff:
                st=Manager.objects.get(email=name)
                request.session['id']=st.id
                return redirect("/manHome")
            else:
                st=Customer.objects.get(email=name)
                request.session['id']=st.id
                return redirect("/userHome")
        else:
            msg="Inavlid username/passsword!"
            return render(request,"login.html",{"msg":msg})
    else:
        return render(request,"login.html",{"msg":msg})
    
def adminHome(request):
    return render(request,"adminHome.html")
    
def adminUser(request):
    data=Customer.objects.filter().order_by("-id")
    return render(request,"adminUser.html",{"data":data})


def adminActiveUser(request):
    id = request.GET['id']
    status = request.GET['status']
    data = User.objects.get(id=id)
    data.is_active = status
    data.save()
    return redirect("/adminUser")

    
def adminManager(request):
    data=Manager.objects.filter().order_by("-id")
    msg = ''
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        district = request.POST['district']
        village = request.POST['village']
        try:
            usr = User.objects.create_user(
                username=email, password=password, is_active=1,is_staff=1)
            usr.save()
            par = Manager.objects.create(
                name=name, email=email, phone=phone, address=address, district=district, village=village, user=usr)
            par.save()
            messages.info(request,'Registartion Successfull..')
        except:
            messages.info(request,'Username already registred..')
            

    else:
        return render(request, 'adminManager.html', {"msg": msg,"data":data})
    return render(request,"adminManager.html",{"data":data})


def adminActiveManager(request):
    id = request.GET['id']
    status = request.GET['status']
    data = User.objects.get(id=id)
    data.is_active = status
    data.save()
    return redirect("/adminManager")


def adminProperties(request):
    id=request.GET['id']
    man=Manager.objects.get(id=id)
    name=man.name
    stay=Stay.objects.filter(user_id=id).order_by("-id")
    return render(request,"adminProperties.html",{"data":stay,"name":name})

def adminBookings(request):
    data=Booking.objects.filter().order_by("-id")
    return render(request,"adminBookings.html",{"data":data})

def adminFeedbacks(request):
    data=Feedback.objects.filter().order_by("-id")
    return render(request,"adminFeedbacks.html",{"data":data})

def userHome(request):
    return render(request,"userHome.html")

def userProperties(request):
    data=Stay.objects.filter().order_by("-id")

    if request.POST:
        song = request.POST["txtSearch"]
        data = Stay.objects.filter(Q(village__contains=song) | Q(district__contains=song)).order_by("-id")
        return render(request, "userProperties.html", {"data": data})
    else:

        return render(request,"userProperties.html",{"data":data})


from datetime import datetime

def userBook(request):
    uid=request.session['id']
    user=Customer.objects.get(id=uid)
    if request.method == "POST":
        id = request.POST['id']
        from_date = request.POST['from']
        to_date = request.POST['to']

        stay = Stay.objects.get(id=id)
        rate = stay.rate
        
        # Convert string dates to datetime objects
        from_date_obj = datetime.strptime(from_date, "%Y-%m-%d")
        to_date_obj = datetime.strptime(to_date, "%Y-%m-%d")

        # Calculate the number of days
        num_days = (to_date_obj - from_date_obj).days

        # Ensure at least 1 day is counted
        total = rate * max(num_days, 1)
      
        bok=Booking.objects.create(user=user,stay=stay,from_date=from_date,to_date=to_date,total=total,status="Requested")
        bok.save()
        messages.info(request,"Request Sent Successfully..")
        return redirect("/userRequests")
        # return redirect(f"/userPay?id={id}&from_d={from_date}&to_d={to_date}")

    return redirect("/userProperties")


def userPay(request):
    
        uid=request.session['id']
        user=Customer.objects.get(id=uid)

        id = request.GET['id']
        bok=Booking.objects.get(id=id)
        total = bok.total

        # stay=bok.stay
        # from_date=bok.from_date
        # to_date=bok.to_date
        if request.POST:
            bok.status="Booked"
            bok.save()
            messages.info(request,"Booking Successfull..")
            return redirect("/userBookings")
    
        return render(request,"userPay.html",{"rate":total})



def userRequests(request):
    uid=request.session['id']
    user=User.objects.get(id=uid)
    data=Booking.objects.filter(user_id=uid,status="Requested").order_by("-id")
    return render(request,"userRequests.html",{"data":data})

def userBookings(request):
    uid=request.session['id']
    user=User.objects.get(id=uid)
    data=Booking.objects.filter(user_id=uid).exclude(status="Requested").order_by("-id")
    return render(request,"userBookings.html",{"data":data})

def userFeedback(request):
    id=request.GET['id']
    bok=Booking.objects.get(id=id)

    if request.POST:
        feedback=request.POST['feedback']

        feed=Feedback.objects.create(book=bok,review=feedback)
        feed.save()
        bok.status="Feedback Completed"
        bok.save()
        messages.info(request,"Feedback Added Successfully..")
        return redirect("/userBookings")

    return render(request,"userFeedback.html")


def manHome(request):
    return render(request,"manHome.html")

def manProperties(request):
    uid=request.session['id']
    
    data=Stay.objects.filter(user_id=uid).order_by("-id")

    man=Manager.objects.get(id=uid)
    user=man.user
    phone=man.phone
    email=man.email
    district=man.district
    village=man.village
    address=man.address

    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        district = request.POST['district']
        village = request.POST['village']
        image=request.FILES['image']

        existing_user = User.objects.filter(username=email).exclude(id=user.id).first()

        if existing_user:
            messages.error(request, "This email is already registered. Please use a different email.")

        else:
            stay=Stay.objects.create(name=name,email=email,phone=phone,address=address,district=district,village=village,image=image,user=man)
            stay.save()
            messages.info(request,"Property added successfully..")
            



    return render(request,"manProperties.html",{"data":data,"phone":phone,"email":email,"district":district,"village":village,"address":address})


def propertyAvailable(request):
    id=request.GET['id']
    status=request.GET['status']
    stay=Stay.objects.get(id=id)
    stay.status=status
    stay.save()
    return redirect("/manProperties")


def manAddAmount(request):
    if request.POST:
        id=request.POST['id']
        rate=request.POST['rate']
        stay=Stay.objects.get(id=id)
        stay.rate=rate
        stay.save()
    return redirect("/manProperties")

def manBookings(request):
    uid=request.session['id']
    data=Booking.objects.filter(stay__user_id=uid,status="Requested").order_by("-id")
    return render(request,"manBookings.html",{"data":data})

def manBookComplete(request):
    uid=request.session['id']
    data=Booking.objects.filter(stay__user_id=uid).exclude(status="Requested").order_by("-id")
    return render(request,"manBookComplete.html",{"data":data})

def manApprove(request):
    uid=request.session['id']
    man=Manager.objects.get(id=uid)
    id=request.GET['id']
    status=request.GET['status']
    book=Booking.objects.get(id=id)
    book.status=status
    book.save()
    return redirect("/manBookings")

def manComplete(request):
    uid=request.session['id']
    man=Manager.objects.get(id=uid)
    id=request.GET['id']
    status=request.GET['status']
    book=Booking.objects.get(id=id)
    book.status=status
    book.save()
    return redirect("/manBookComplete")

def manFeedbacks(request):
    uid=request.session['id']
    data=Feedback.objects.filter(book__stay__user_id=uid).order_by("-id")
    return render(request,"manFeedbacks.html",{"data":data})