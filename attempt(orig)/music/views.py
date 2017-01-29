from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import UserForm
from django.contrib.auth.models import User

def index(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        return render(request, 'music/base_visitor.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'music/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                
                return render(request, 'music/base.html')
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login.html')


def register(request):
    form = UserForm(request.POST or None)
    login_statement=None    
    reg_statement=None
    if request.method == 'POST' and 'signup' in request.POST:
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')     
        if username:
            try:
                u=User.objects.get(username=username)
                reg_statement="Username already taken!"
            except:#in case username is unique.
                if password!=confirmpassword:

                    reg_statement="Password doesn't match!"
                else:#username and password are accepted
                    user = User.objects.create_user(username=username,email=email)
                    user.first_name = firstname
                    user.last_name = lastname
                    user.set_password(password)
                    user.save()
                    user = authenticate(username=username, password=password)
                    name = firstname + ' ' + lastname 
                    login(request, user)
                
                    return render(request, 'music/login.html')
    context = {
        'login_statement':login_statement,
        'reg_statement':reg_statement,
        "form": form,
    }
    return render(request, 'music/register.html', context)





