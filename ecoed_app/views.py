from django.shortcuts import render, redirect
from .models import Book, User, Subscriber, Carbon
from django.contrib import messages
import bcrypt
from datetime import date

def filter_by_date():
    todays_date=date.today()
    book=Book.objects.filter(
        month__year=todays_date.year,
        month__month=todays_date.month
        )
    print(book)
    if len(book)>0:
        return book[0]
    else:
        # return an empty array
        book=[]
        return book

def index(request):
    book_otm = filter_by_date
    context = {
        'books': Book.objects.all(),
        'book_otm': book_otm,
    }
    return render(request, 'index.html', context)

# /ecoed/registration
def reg_user(request):
    return render(request, 'reg.html')

# /ecoed/create_user
def create_user(request):
    errors = User.objects.reg_validate(request.POST)
    if len(errors)>0:
        for k,v in errors.items():
            messages.error(request,v)
        return redirect('/ecoed/registration')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        active_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            bday = request.POST['bday'],
            password = pw_hash
        )
        request.session['user_id']=active_user.id
        Carbon.objects.create(
            flights = 0,
            drives = 0,
            trains = 0,
            fp_user = active_user
        )
        return redirect(f'/ecoed/hello/{active_user.first_name}')

# /ecoed/login
def login_user(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    email_active = User.objects.filter(email=request.POST['email'])
    if email_active:
        errors = User.objects.login_validate(request.POST)
        if len(errors)>0:
            for k,v in errors.items():
                messages.error(request,v)
            return redirect('/ecoed/login')
        else:
            active_user = email_active[0]
            if bcrypt.checkpw(request.POST['password'].encode(), active_user.password.encode()):
                request.session['user_id']=active_user.id
                return redirect(f'/ecoed/hello/{active_user.first_name}')
    messages.error(request, 'Invalid user email or password')
    return redirect('/ecoed/login')

# /ecoed/logout
def logout(request):
    request.session.flush()
    return redirect('/ecoed')

# /ecoed/subscribe
def subscribe(request):
    if request.method == 'GET':
        return render(request, 'subscribe.html')
    errors = User.objects.login_validate(request.POST)
    if len(errors)>0:
        for k,v in errors.items():
            messages.error(request,v)
        return redirect('/ecoed/subscribe')
    Subscriber.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email']
    )
    return redirect('/ecoed')

# /ecoed/hello/<str:user_fname>
def user_home(request, user_fname):
    active_user = User.objects.get(id=request.session['user_id'])
    carbon_fp = active_user.carbon_footprint.all()[0]
    flight_C = carbon_fp.flights*53
    drive_C = carbon_fp.drives*0.9
    train_C = carbon_fp.trains*0.15
    context = {
        'user': active_user,
        'book_otm': filter_by_date(),
        # mileage
        'flights': carbon_fp.flights,
        'drives': carbon_fp.drives,
        'trains': carbon_fp.trains,
        # carbon total
        'flight_C': flight_C,
        'drive_C': drive_C,
        'train_C': train_C,
    }
    return render(request, 'user_home.html', context)

# /ecoed/carbon/log
def log_carbon(request):
    active_user = User.objects.get(id=request.session['user_id'])
    # edit user model for drive and flight total mileage
    carbon = active_user.carbon_footprint.all()[0]
    if request.POST['activity']=='plane':
        carbon.flights += int(request.POST['mileage'])
        carbon.save()
        return redirect(f'/ecoed/hello/{active_user.first_name}')
        #log flight carbon * miles
    if request.POST['activity']=='car':
        carbon.drives += int(request.POST['mileage'])
        carbon.save()
        #log drive carbon * miles
        return redirect(f'/ecoed/hello/{active_user.first_name}')
    if request.POST['activity']=='train':
        carbon.trains += int(request.POST['mileage'])
        carbon.save()
        return redirect(f'/ecoed/hello/{active_user.first_name}')
    else:
        messages.error(request, 'Select method of transport')
    return redirect(f'/ecoed/hello/{active_user.first_name}')

# /ecoed/books/<int:book_id>
def view_book(request, book_id):
    context = {
        'book': Book.objects.get(id=book_id)
    }
    return render(request, 'book.html', context)