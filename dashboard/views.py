from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required, hr_required, employee_required

@login_required
@admin_required
def admin_dashboard(request):
    return render(request,"dashboard/admin.html")

@login_required
@hr_required
def hr_dashboard(request):
    return render(request,"dashboard/hr.html")

@login_required
@employee_required
def employee_dashboard(request):
    return render(request,"dashboard/employee.html")