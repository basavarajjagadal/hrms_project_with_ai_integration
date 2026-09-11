from django.shortcuts import redirect,render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import admin_required
from .models import User
from django.core.mail import send_mail


def login_view(request):
    print("1")
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        print("2")
        user=authenticate(request,username=username,password=password)
        print("3")
        if user is not None:
            login(request,user)
            print("4")
            if user.role=="admin":
                print("5")
                return redirect("admin_dashboard")
            
            elif user.role=="hr":
                print("5")
                return redirect("hr_dashboard")
            elif user.role=="employee":
                print("5")
                return redirect("employee_dashboard")
            

            return render(request, "accounts/login.html", {"error": "Invalid credentials"})
    return render(request,"accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")

@admin_required
def admin_profile(request):
    user=request.user
    return render(request,"accounts/admin_profile.html",{"user":user})

@admin_required
def edit_admin_profile(request):
    user=request.user
    if request.method =="POST":
        user.username=request.POST.get("username")
        user.email=request.POST.get("email")
        user.save()
        return redirect("admin_profile")
        

    return render(request,"accounts/edit_admin_profile.html",{"user":user})


# here admin can view all hrs and add new hr
@admin_required
@login_required
def hrsmenu(request):

    return render(request,"accounts/hrmenu.html")

@admin_required
@login_required
def viewallhrs(request):
    print("hi")
    hrs =User.objects.filter(role="hr")
    print("hi")
    return render(request,"accounts/all_hrs.html",{"hrs":hrs})

@login_required
@admin_required
def addhr(request):
    print("hi")
    if request.method =="POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")

        user=User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role="hr"
        )

        send_mail(
            subject="Your HRMS Login Credentials",
            message=f"""
        Welcome to HRMS.

        Your account has been created.

        Username: {username}
        Password: {password}

        Login here:
        http://127.0.0.1:8000/accounts/login/
        """,
            from_email="basavarajjagadal17@gmail.com",
            recipient_list=[email],
            fail_silently=False,
        )
        return redirect('hrsmenu')
        


    return render(request,"accounts/addhr.html")