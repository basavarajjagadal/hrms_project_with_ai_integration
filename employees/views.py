from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import employee_required, hr_required, admin_required
from .models import Employee
from accounts.models import User

from django.core.mail import send_mail

@login_required
@employee_required
def employee_profile(request):

    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        context = {
            'user': request.user,
        }
        return render(request, 'employees/profile.html', context)
    
    context = {
        'employee': employee,
        'user': request.user
    }
    
    return render(request, 'employees/profile.html', context)


@login_required
@employee_required
def edit_profile(request):
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        
        context = {
            'user': request.user,
            'error': 'Employee profile not found.'
        }
        return render(request, 'employees/edit_profile.html', context)
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        
        if first_name and last_name and email:
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.email = email
            request.user.save()
            return redirect('employee_profile')
        else:
            messages.error(request, 'All fields are required')
    
    context = {
        'employee': employee,
        'user': request.user
    }
    
    return render(request, 'employees/edit_profile.html', context)


@login_required
@hr_required
def employee_list(request):
    employees = Employee.objects.all().select_related('user')
    
    # Filter by department if provided
    department = request.GET.get('department')
    if department:
        employees = employees.filter(department__icontains=department)
    
    context = {
        'employees': employees,
    }
    
    return render(request, 'employees/employee_list.html', context)


@login_required
@hr_required
def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    
    context = {
        'employee': employee,
    }
    
    return render(request, 'employees/employee_detail.html', context)


@login_required
@hr_required
def menu(request):
    return render(request,'employees/employees_menu.html')

@login_required
@hr_required
def hr_profile(request):

    context = {
        'user': request.user
    }
    return render(request, 'employees/hr_profile.html', context)

@login_required
@hr_required
def edit_hr_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        
        if first_name and last_name and email:
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.email = email
            request.user.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('hr_profile')
        else:
            messages.error(request, 'All fields are required')

    context = {
        'user': request.user
    }
    return render(request, 'employees/edit_hr_profile.html', context)

@login_required
@hr_required
def adduser_employee(request):
    if request.method=="POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")

        user=User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role="employee"
        )


        employee_id=request.POST.get("employee_id")
        department=request.POST.get("department")
        designation=request.POST.get("designation")
        joining_date=request.POST.get("joining_date")

        Employee.objects.create(
            user=user,
            employee_id=employee_id,
            department=department,
            designation=designation,
            joining_date=joining_date
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

        return redirect("/employees/")

    return render(request,'employees/create_user.html')





# admins
@login_required
@admin_required
def manage_employees(request):

    
    employees=Employee.objects.select_related('user').all()
    print("hi")

    return render(request,'employees/manage_employees.html',{"employees":employees})


def edit_employees(request,id):
    print("1")
    employee=get_object_or_404(Employee,id=id)
    print("2")
    if request.method=="POST":
        employee.department=request.POST.get("department")
        employee.designation=request.POST.get("designation")
        joining_date=request.POST.get("joining_date")
        if joining_date:
            employee.joining_date=joining_date
        employee.save()
        return redirect('manage_employees')
    
    print("3")
    return render(request,'employees/edit_employee.html',{"employee":employee})


def delete_employee(request,id):
    employee=get_object_or_404(Employee,id=id)
    employee.user.delete()
    return redirect('manage_employees')
