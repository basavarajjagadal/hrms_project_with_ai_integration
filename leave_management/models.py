from django.db import models

# Create your models here.

class LeaveRequest(models.Model):

    employee=models.ForeignKey('employees.Employee' , on_delete=models.CASCADE,related_name='leave_requests')

    start_date=models.DateField()

    end_date=models.DateField()

    reason=models.TextField()

    STATUS_CHOICES =(
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    status=models.CharField(max_length=20, choices=STATUS_CHOICES ,default='pending')

    def __str__(self):
        return f"{self.employee.user.username} - {self.status}"