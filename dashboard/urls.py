
from django.urls import path
from . import views

urlpatterns = [
    path('admin/',views.admin_dashboard,name='admin_dashboard'),
    path('hr/',views.hr_dashboard,name='hr_dashboard'),
    path('employee/',views.employee_dashboard,name='employee_dashboard')
  

]