from django.db import models

# Create your models here.

class Onboarding(models.Model):

    employee=models.OneToOneField('employees.Employee' , on_delete=models.CASCADE,related_name='onboarding')

    id_proof_submitted=models.BooleanField(default=False)

    bank_details_added=models.BooleanField(default=False)

    hr_verified=models.BooleanField(default=False)

    laptop_assigned=models.BooleanField(default=False)

    STATUS_CHOICES =(
        ('pending', 'Pending'),
        ('in_progress', 'In_Progress'),
        ('completed', 'Completed'),
    )

    status=models.CharField(max_length=20, choices=STATUS_CHOICES ,default='pending')

    def __str__(self):
        return f"{self.employee.user.username} - {self.status}"

class IDProof(models.Model):

    employee=models.OneToOneField('employees.Employee' , on_delete=models.CASCADE,related_name='id_proof')

    ID_TYPES=(
        ('adhar', 'Adhar'),
        ('pan', 'Pan'),
        ('passport', 'Passport'),
    )

    id_type=models.CharField(max_length=20, choices=ID_TYPES)

    id_number=models.CharField(max_length=50)

    document=models.FileField(upload_to='id_proofs/')

    uploaded_at=models.DateTimeField(auto_now_add=True)


class BankDetails(models.Model):

    employee=models.OneToOneField('employees.Employee' , on_delete=models.CASCADE)

    bank_name=models.CharField(max_length=100)

    account_number=models.CharField(max_length=20)

    ifsc_code=models.CharField(max_length=20)



class Verification(models.Model):

    employee=models.OneToOneField('employees.Employee' , on_delete=models.CASCADE,related_name='verification')

    verified=models.BooleanField(default=False)

    verified_by=models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True,related_name='verified_employees')

    verified_at=models.DateTimeField(null=True, blank=True)


class LaptopAllocation(models.Model):

    employee=models.OneToOneField('employees.Employee' , on_delete=models.CASCADE,related_name='laptop')

    laptop_serial=models.CharField(max_length=100)

    issued_date=models.DateField()

    issued_by=models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True,related_name='issued_laptops')



    
