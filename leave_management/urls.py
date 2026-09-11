
from django.urls import path
from . import views

urlpatterns= [
    path('', views.leave_menu, name='leave_menu'),
    path('apply/', views.apply_leave, name='apply_leave'),
    path('status/', views.leave_status, name='leave_status'),
    path('cancel/<int:leave_id>/', views.cancel_leave, name='cancel_leave'),
    
    path('hr/',views.hr_leave_menu,name='hr_leave_menu'),

    path('hr/approve/<int:leave_id>/', views.approve_leave, name='approve_leave'),
    path('hr/reject/<int:leave_id>/', views.reject_leave, name='reject_leave'),
    path('hr/pending/<int:leave_id>/', views.pending_leave, name='pending_leave'),

    # admin
    path('allleaverequest/',views.allleaverequest,name='allleaverequest')
]   