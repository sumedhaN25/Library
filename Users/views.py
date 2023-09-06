from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib.auth import login, authenticate, logout #add this
from django.contrib.auth.forms import AuthenticationForm #add this



# Create your views here.


def register_request(request):
    if request.method == "POST":
        print(request.POST)
        form = NewUserForm(request.POST)
        if form.is_valid():
            print("In if condition")
            user = form.save()
            # login(request, user)
            return redirect("register")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})



def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("main:homepage")
            else:
                pass
        else:
            pass
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})



def logout_user(request):
    logout(request)  
    return redirect("login_user")

