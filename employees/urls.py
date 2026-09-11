from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.employee_profile, name='employee_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
    path('list/', views.employee_list, name='employee_list'),
    path('detail/<int:employee_id>/', views.employee_detail, name='employee_detail'),
    
    path('',views.menu,name='menu'),

    path('hr_profile/',views.hr_profile,name='hr_profile'),
    path('edit_hr_profile/',views.edit_hr_profile,name='edit_hr_profile'),

    path('add/',views.adduser_employee,name='add_user_employee'),


    path('manage/',views.manage_employees,name='manage_employees'),
    path('edit/<int:id>',views.edit_employees,name='edit_employees'),
    path('delete/<int:id>', views.delete_employee,name='employee_delete')
    
]