from django.urls import path
from . import views

from django.contrib.auth import views as auth_views 

urlpatterns= [
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    
    path('profile/', views.admin_profile, name='admin_profile'),
    path('edit-profile/', views.edit_admin_profile, name='edit_admin_profile'),

    # view hr and add hr
    path('hrsmenu/',views.hrsmenu,name='hrsmenu'),
    path('hrs/',views.viewallhrs,name='hrs'),
    path('add-hr/',views.addhr,name='addhr'),
    
    path('reset_password/',auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),    


    
]