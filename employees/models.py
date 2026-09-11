from django.db import models

# Create your models here.

class Employee(models.Model):

    user=models.OneToOneField('accounts.User', on_delete=models.CASCADE,related_name='employee')

    employee_id=models.CharField(max_length=20, unique=True)

    department=models.CharField(max_length=100)

    designation=models.CharField(max_length=100)

    joining_date=models.DateField()

    def __str__(self):
        return self.user.username