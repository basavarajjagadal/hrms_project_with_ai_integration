from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from accounts.decorators import employee_required, hr_required
from employees.models import Employee
from .models import LeaveRequest
from accounts.decorators import admin_required
from django.core.mail import send_mail
from django.conf import settings 

def send_leave_email(leave_request):
    
    user=leave_request.employee.user
    
    subject="Leave Request Update"
    
    message=f"""
    Dear {user.username},
    
    Your leave request from {leave_request.start_date} to {leave_request.end_date} has been {leave_request.status.upper()}.
    
    Reason: {leave_request.reason}
    
    Regards,
    HR Team
    """
    
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],  
        fail_silently=False,
    )
    
    
    
@login_required
@employee_required
def leave_menu(request):
    context = {}
    return render(request, 'leave_management/menu.html', context)

@login_required
@employee_required
def apply_leave(request):
    
    total_leaves=20
    employee=Employee.objects.get(user=request.user)
    leaves_takenby_employee=calculate(employee)
    remaining_days=total_leaves-leaves_takenby_employee
    print(remaining_days)
    

    if request.method == "POST":

        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        reason = request.POST.get("reason")

        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()

        if start_date_obj > end_date_obj:
            return render(request, "leave/apply_leave.html", {
                "error": "Start date cannot be after end date"
            })

        LeaveRequest.objects.create(
            employee=employee,
            start_date=start_date_obj,
            end_date=end_date_obj,
            reason=reason
        )

        return redirect("employee_dashboard")
    
    return render(request, 'leave_management/apply_leave.html',{"remaining_days":remaining_days})


# helper to auto-reject any pending requests whose end date has passed

def expire_pending_leaves():
    today = timezone.now().date()
    expired = LeaveRequest.objects.filter(status='pending', start_date__lt=today)
    for lr in expired:
        lr.status = 'rejected'
        lr.save()


@login_required
@employee_required
def leave_status(request):
    employee = Employee.objects.get(user=request.user)

    leaves = LeaveRequest.objects.filter(employee=employee).order_by('-start_date')

    check_expired_leaves = leaves.filter(status='pending', start_date__lt=timezone.now().date())
    for leave in check_expired_leaves:
        leave.status = 'rejected'
        leave.save()
    
    pending_count = leaves.filter(status="pending").count()
    approved_count = leaves.filter(status="approved").count()
    rejected_count = leaves.filter(status="rejected").count()

    return render(request, "leave_management/status.html", {
        "leaves": leaves,
        "pending_count": pending_count,
        "approved_count": approved_count,
        "rejected_count": rejected_count
    })
    

@login_required
@employee_required
def cancel_leave(request, leave_id):
    leave_request = get_object_or_404(LeaveRequest, id=leave_id)
    
    if leave_request.employee.user != request.user:
        messages.error(request, 'You do not have permission to cancel this leave')
        return redirect('leave_status')
    
    if leave_request.status == 'pending':
        leave_request.delete()
    
    return redirect('leave_status')

def calculate(employee):
    
    leave_record=LeaveRequest.objects.filter(employee=employee,status='approved')

    total_days=0
    for leave in leave_record:
        total_days+=(leave.end_date-leave.start_date).days+1

    return total_days

@login_required
@hr_required
def hr_leave_menu(request):
    expire_pending_leaves()

    leaves = LeaveRequest.objects.select_related(
        'employee__user'
    ).all()

    for leave in leaves:
        leave.days = (leave.end_date - leave.start_date).days + 1

    return render(request, 'leave_management/leave_request.html', {
        "leaves": leaves
    })

@login_required
@hr_required
def approve_leave(request, leave_id):
    if request.method == 'POST':
        leave_request = get_object_or_404(LeaveRequest, id=leave_id)
        leave_request.status = 'approved'
        leave_request.save()
        
        send_leave_email(leave_request)
        
    return redirect('hr_leave_menu')

@login_required
@hr_required
def reject_leave(request, leave_id):
    if request.method == 'POST':
        leave_request = get_object_or_404(LeaveRequest, id=leave_id)
        leave_request.status = 'rejected'
        leave_request.save()
        
        send_leave_email(leave_request)
        
    return redirect('hr_leave_menu')

@login_required
@hr_required
def pending_leave(request, leave_id):
    if request.method == 'POST':
        leave_request = get_object_or_404(LeaveRequest, id=leave_id)
        leave_request.status = 'pending'
        leave_request.save()
    return redirect('hr_leave_menu')


@login_required
@admin_required
def allleaverequest(request):
    leaves=LeaveRequest.objects.all().order_by('-start_date')
    return render(request,"leave_management/allleaverequest.html",{"leaves":leaves})
    
