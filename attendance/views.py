


from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, timedelta
from accounts.decorators import employee_required,hr_required,admin_required
from employees.models import Employee
from .models import Attendence
from django.utils.dateparse import parse_time
from django.core.paginator import Paginator

@login_required
@employee_required
def attendance_menu(request):
    context = {}
    return render(request, 'attendance/menu.html', context)


@login_required
@employee_required
def check_in_out(request):   
    employee = Employee.objects.get(user=request.user)

    today = timezone.now().date()

    attendance = Attendence.objects.filter(
        employee=employee,
        date=today
    ).first() 
    return render(request, 'attendance/check_in_out.html',{"attendance":attendance})


@login_required
@employee_required
def attendance_history(request):
    employee = Employee.objects.get(user=request.user)

    records = Attendence.objects.filter(
        employee=employee
    ).order_by('-date')

    date = request.GET.get('date')
    month = request.GET.get('month')
    year = request.GET.get('year')

    if date:
        records = records.filter(date=date)

    if month:
        records = records.filter(date__month=month)

    if year:
        records = records.filter(date__year=year)
    
    return render(request, 'attendance/history.html', {"records":records})

@login_required
@hr_required
def menu(request):
    return render(request, 'attendance/hrmenu_attendance.html')


@login_required
@hr_required
def checktodayattendance(request):

    today = timezone.now().date()
    total_employees = Employee.objects.count()

    today_records = Attendence.objects.filter(date=today)
    present_count = today_records.filter(status='present').count()
    leave_count = today_records.filter(status='leave').count()
    recorded_absent = today_records.filter(status='absent').count()

    missing_count = total_employees - today_records.count()
    absent_count = recorded_absent + max(0, missing_count)

    context = {
        'today': today,
        'total_employees': total_employees,
        'present_count': present_count,
        'absent_count': absent_count,
        'leave_count': leave_count,
        'recorded_absent': recorded_absent,
        'missing_count': missing_count,
    }

    return render(request,'attendance/todayattandance.html',context)


@login_required
@hr_required
def today_attendance_details(request):

    print("1")

    today = timezone.now().date()

    print("2")

    employees = Employee.objects.select_related('user').all()

    print("3")

    attendance_records = []

    print("4")

    for emp in employees:

        attendance = Attendence.objects.filter(
            employee=emp,
            date=today
        ).first()

        print("5")

        attendance_records.append({
            "employee": emp,
            "attendance": attendance
        })

        print("6")

    return render(request, "attendance/today_attendance_details.html", {
        "attendance_records": attendance_records,
        "today": today
    })

@login_required
@hr_required
def mark_attendance(request, employee_id):
    time = timezone.now().date()

    employee = get_object_or_404(Employee, id=employee_id)

    attendance = Attendence.objects.filter(
        employee=employee,
        date=time
    ).first()

    if request.method == "POST":
        status = request.POST.get("status")
        check_in_str = request.POST.get("check_in")
        check_out_str = request.POST.get("check_out")

        check_in = parse_time(check_in_str) if check_in_str else None
        check_out = parse_time(check_out_str) if check_out_str else None

        attendance, created = Attendence.objects.get_or_create(
            employee=employee,
            date=time,
            defaults={
                'status': status,
                'check_in_time': check_in,
                'check_out_time': check_out
            }
        )

        if not created:
            attendance.status = status
            attendance.check_in_time = check_in
            attendance.check_out_time = check_out
            attendance.save()

        return redirect('today_attendance_details')

    return render(request, 'attendance/mark_attendance.html', {
        "employee": employee,
        "date": time,
        "attendance": attendance
    })
        



# in admin attendence records
@login_required
def attendencerecords(request):

    records = Attendence.objects.select_related(
        'employee__user'
    ).all().order_by('-date')
    
    for record in records:
        if record.check_in_time and record.check_out_time:
            duration = datetime.combine(record.date, record.check_out_time) - \
                    datetime.combine(record.date, record.check_in_time)
                    
            print(duration )

            total_seconds = duration.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            print(hours, minutes)

            record.worked_hours = hours
            record.worked_minutes = minutes
        else:
            record.worked_hours = 0
            record.worked_minutes = 0            
    
    employees = Employee.objects.all()

    date = request.GET.get('date')
    month = request.GET.get('month')
    year = request.GET.get('year')
    employee = request.GET.get('employee')
    status = request.GET.get('status')

    if date:
        records = records.filter(date=date)

    if month:
        records = records.filter(date__month=month)

    if year:
        records = records.filter(date__year=year)

    if employee:
        records = records.filter(employee_id=employee)

    if status:
        records = records.filter(status=status)

    paginator=Paginator(records,10)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    context = {
        "employees": employees,
        "page_obj": page_obj
    }
    
    return render(request, "attendance/attendencerecords.html", context)


@login_required
def check_in(request):

    employee = Employee.objects.get(user=request.user)

    today = timezone.now().date()

    attendance, created = Attendence.objects.get_or_create(
        employee=employee,
        date=today
    )

    if attendance.check_in_time:
        return redirect("employee_dashboard")

    attendance.status = "present"
    attendance.check_in_time = timezone.now().time()
    attendance.save()

    return redirect("employee_dashboard")



@login_required
def check_out(request):

    employee = Employee.objects.get(user=request.user)

    today = timezone.now().date()

    attendance = Attendence.objects.get(
        employee=employee,
        date=today
    )
    if not attendance.check_in_time:
        return redirect("employee_dashboard")

    attendance.check_out_time = timezone.now().time()
    attendance.save()

    return redirect("employee_dashboard")

from reportlab.platypus import SimpleDocTemplate,Table,TableStyle,Paragraph,Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

from django.http import HttpResponse

# pdf generating function
def attendance_pdf(request):
    user= request.user
    employee=user.employee
    
    records=Attendence.objects.filter(employee=employee).order_by('date')
    
    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='attachment; filename="attendance_report.pdf"'
    
    doc=SimpleDocTemplate(response,pagesize=A4)
    elements=[]
    
    styles=getSampleStyleSheet()
    
    elements.append(Paragraph("Attendance Report", styles['Title']))
    elements.append(Spacer(1, 10))
    
    elements.append(Paragraph(f"Name: {user.username}", styles['Normal']))
    elements.append(Paragraph(f"Employee ID: {employee.employee_id}", styles['Normal']))
    elements.append(Paragraph(f"Department: {employee.department}", styles['Normal']))
    elements.append(Spacer(1, 10))
    
    total_days = records.count()
    present_days = records.filter(status='present').count()
    absent_days = records.filter(status='absent').count()
    leave_days = records.filter(status='leave').count()
    
    elements.append(Paragraph(f"Total Days: {total_days}", styles['Normal']))
    elements.append(Paragraph(f"Present: {present_days}", styles['Normal']))
    elements.append(Paragraph(f"Absent: {absent_days}", styles['Normal']))
    elements.append(Paragraph(f"Leave: {leave_days}", styles['Normal']))
    elements.append(Spacer(1, 15))
    
    data = [["Date", "Check In", "Check Out", "Status"]]

    for record in records:
        date = record.date.strftime("%d-%m-%Y")

        check_in = record.check_in_time.strftime("%H:%M") if record.check_in_time else "-"
        check_out = record.check_out_time.strftime("%H:%M") if record.check_out_time else "-"

        status = record.status.upper()

        data.append([date, check_in, check_out, status])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))

    elements.append(table)

    doc.build(elements)

    return response
    