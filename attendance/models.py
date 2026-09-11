from django.db import models

# Create your models here.


class Attendence(models.Model):

    employee=models.ForeignKey('employees.Employee' , on_delete=models.CASCADE,related_name='attendences')

    date=models.DateField()

    check_in_time = models.TimeField(null=True, blank=True)

    check_out_time=models.TimeField(null=True, blank=True)

    STATUS_CHOICES =(
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('leave', 'Leave'),
    )

    status=models.CharField(max_length=20,choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.employee.user.username} - {self.status} - {self.date}"