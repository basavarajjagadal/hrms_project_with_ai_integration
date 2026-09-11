from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from accounts.decorators import employee_required, hr_required
from employees.models import Employee
from .models import Onboarding, IDProof, BankDetails, Verification, LaptopAllocation


@login_required
@employee_required
def onboarding_status(request):
    
    employee = get_object_or_404(Employee, user=request.user)

    onboarding, created = Onboarding.objects.get_or_create(employee=employee)

    has_id_proof = IDProof.objects.filter(employee=employee).exists()

    has_bank_details = BankDetails.objects.filter(employee=employee).exists()

    context = {
        
        "employee": employee,
        "onboarding": onboarding,
        "has_id_proof": has_id_proof,
        "has_bank_details": has_bank_details,
    }

    return render(request, "onboarding/onboarding_status.html", context)
    

@login_required
@employee_required
def upload_id_proof(request):

    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        return redirect('employee_dashboard')
    
    id_proof = IDProof.objects.filter(employee=employee).first()
    
    if request.method == 'POST':
        id_type = request.POST.get('id_type')
        id_number = request.POST.get('id_number')
        document = request.FILES.get('document')
        
        if id_type and id_number and document:
            if id_proof:
                id_proof.id_type = id_type
                id_proof.id_number = id_number
                id_proof.document = document
                id_proof.save()
                messages.success(request, 'ID proof updated successfully')
            else:
                IDProof.objects.create(
                    employee=employee,
                    id_type=id_type,
                    id_number=id_number,
                    document=document
                )

            
            onboarding = Onboarding.objects.get_or_create(employee=employee)[0]
            onboarding.id_proof_submitted = True
            onboarding.status = 'in_progress'
            onboarding.save()
            
            return redirect('onboarding_status')
        else:
            messages.error(request, 'All fields are required')
    
    context = {
        'employee': employee,
        'id_proof': id_proof,
        'id_types': IDProof._meta.get_field('id_type').choices
    }
    
    return render(request, 'onboarding/upload_id.html', context)


@login_required
@employee_required
def add_bank_details(request):

    employee = request.user.employee

    bank_details = BankDetails.objects.filter(employee=employee).first()
    
    if request.method == 'POST':
        
        bank_name = request.POST.get('bank_name')
        account_number = request.POST.get('account_number')
        ifsc_code = request.POST.get('ifsc_code')
        

        if bank_details:
            
            bank_details.bank_name = bank_name
            bank_details.account_number = account_number
            bank_details.ifsc_code = ifsc_code
            bank_details.save()
        else:
            BankDetails.objects.create(
                employee=employee,
                bank_name=bank_name,
                account_number=account_number,
                ifsc_code=ifsc_code
            )            

        onboarding, _ = Onboarding.objects.get_or_create(employee=employee)
        onboarding.bank_details_added = True
        onboarding.status = 'in_progress'
        onboarding.save()
            
        return redirect('onboarding_status')

    
    context = {
        'bank_details': bank_details
    }
    
    return render(request, 'onboarding/bank_details.html', context)


@login_required
def onboarding_verification(request):

    try:
        employee = Employee.objects.get(user=request.user)
        onboarding = Onboarding.objects.get_or_create(employee=employee)[0]
    except Employee.DoesNotExist:
        return redirect('employee_dashboard')
    
    context = {
        'employee': employee,
        'onboarding': onboarding,
    }
    
    return render(request, 'onboarding/verify_documents.html', context)



@login_required
@hr_required
def hr_add_onboarding(request):

    employees = Employee.objects.filter(onboarding__isnull=True)
    print(employees.query)

    if request.method == 'POST':
        emp_id = request.POST.get('employee')
        if emp_id:
            employee = get_object_or_404(Employee, id=emp_id)
            onboarding = Onboarding.objects.create(employee=employee)
            return redirect('hr_onboarding_detail', onboarding_id=onboarding.id)
        else:
            messages.error(request, 'Please select an employee to add.')

    context = {
        'employees': employees,
    }
    return render(request, 'onboarding/hr_add_onboarding.html', context)


@login_required
@hr_required
def hr_onboarding_list(request):

    onboardings = Onboarding.objects.all().select_related('employee__user').order_by('-id')
    status = request.GET.get('status')

    if status:
        onboardings = onboardings.filter(status=status)
    
    context = {
        'onboardings': onboardings,
    }
    
    return render(request, 'onboarding/hr_onboarding_list.html', context)


@login_required
@hr_required
def hr_onboarding_detail(request, onboarding_id):

    onboarding = get_object_or_404(Onboarding, id=onboarding_id)
    employee = onboarding.employee
    

    id_proof = IDProof.objects.filter(employee=employee).first()
    bank_details = BankDetails.objects.filter(employee=employee).first()
    verification = Verification.objects.filter(employee=employee).first()
    laptop_allocation = LaptopAllocation.objects.filter(employee=employee).first()
    
    context = {
        'onboarding': onboarding,
        'employee': employee,
        'id_proof': id_proof,
        'bank_details': bank_details,
        'verification': verification,
        'laptop_allocation': laptop_allocation,
    }
    
    return render(request, 'onboarding/hr_onboarding_detail.html', context)


@login_required
@hr_required
def hr_verify_documents(request, onboarding_id):

    onboarding = get_object_or_404(Onboarding, id=onboarding_id)
    employee = onboarding.employee
    
    if request.method == 'POST':

        verification, created = Verification.objects.get_or_create(
            employee=employee,          
            defaults={'verified': True, 'verified_by': request.user}
        )

        if not created:
            verification.verified = True
            verification.verified_by = request.user
            verification.verified_at = timezone.now()
            verification.save()

        onboarding.hr_verified = True

        if onboarding.id_proof_submitted and onboarding.bank_details_added:
            onboarding.status = 'completed'

        else:
            onboarding.status = 'in_progress'
        onboarding.save()
        
        return redirect('hr_onboarding_detail', onboarding_id=onboarding.id)
    
    context = {
        'onboarding': onboarding,
        'employee': employee,
    }
    
    return render(request, 'onboarding/hr_verify_documents.html', context)


@login_required
@hr_required
def hr_assign_laptop(request, onboarding_id):

    onboarding = get_object_or_404(Onboarding, id=onboarding_id)
    employee = onboarding.employee
    
    laptop_allocation = LaptopAllocation.objects.filter(employee=employee).first()
    
    if request.method == 'POST':
        laptop_serial = request.POST.get('laptop_serial')
        issued_date = request.POST.get('issued_date')
        
        if laptop_serial and issued_date:
            if laptop_allocation:
                laptop_allocation.laptop_serial = laptop_serial
                laptop_allocation.issued_date = issued_date
                laptop_allocation.issued_by = request.user
                laptop_allocation.save()
            else:
                LaptopAllocation.objects.create(
                    employee=employee,
                    laptop_serial=laptop_serial,
                    issued_date=issued_date,
                    issued_by=request.user
                )
            
            onboarding.laptop_assigned = True

            if onboarding.id_proof_submitted and onboarding.bank_details_added and onboarding.hr_verified:
                onboarding.status = 'completed'
            else:
                onboarding.status = 'in_progress'
            onboarding.save()
            
            return redirect('hr_onboarding_detail', onboarding_id=onboarding.id)
        else:
            messages.error(request, 'All fields are required')
    
    context = {
        'onboarding': onboarding,
        'employee': employee,
        'laptop_allocation': laptop_allocation,
    }
    
    return render(request, 'onboarding/hr_assign_laptop.html', context)


@login_required
@hr_required
def hr_complete_onboarding(request, onboarding_id):
  
    onboarding = get_object_or_404(Onboarding, id=onboarding_id)
    
    if request.method == 'POST':
        onboarding.status = 'completed'
        onboarding.save()
        return redirect('hr_onboarding_list')
    
    context = {
        'onboarding': onboarding,
        'employee': onboarding.employee,
    }
    
    return render(request, 'onboarding/hr_complete_onboarding.html', context)




def allonboardingstatus(request):
    onboardings=Onboarding.objects.all().select_related('employee__user').order_by('-id')
    return render(request,"onboarding/allonboardingstatus.html",{"onboardings":onboardings})
    