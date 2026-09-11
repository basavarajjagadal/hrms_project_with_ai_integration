
from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_menu, name='attendance_menu'),
    path('check-in-out/', views.check_in_out, name='check_in_out'),
    path('history/', views.attendance_history, name='attendance_history'),
    path('menu/',views.menu,name='menu'),
    path('todayattandance/',views.checktodayattendance,name='todayattandance'),
    path('today-details/', views.today_attendance_details, name='today_attendance_details'),
    path('mark/<int:employee_id>/', views.mark_attendance, name='mark_attendance'),

    path("check-in/", views.check_in, name="check_in"),
    path("check-out/", views.check_out, name="check_out"),

    path('records/',views.attendencerecords,name='attendencerecords'),
    
    # pdf urls 
    path('pdf/', views.attendance_pdf, name='attendance_pdf')



    
]