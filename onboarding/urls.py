
from django.urls import path
from . import views

urlpatterns = [

    path('status/', views.onboarding_status, name='onboarding_status'),
    path('upload-id/', views.upload_id_proof, name='upload_id_proof'),
    path('bank-details/', views.add_bank_details, name='add_bank_details'),
    path('verification/', views.onboarding_verification, name='onboarding_verification'),
    

    path('hr/add/', views.hr_add_onboarding, name='hr_add_onboarding'),
    path('hr/list/', views.hr_onboarding_list, name='hr_onboarding_list'),
    path('hr/detail/<int:onboarding_id>/', views.hr_onboarding_detail, name='hr_onboarding_detail'),
    path('hr/verify/<int:onboarding_id>/', views.hr_verify_documents, name='hr_verify_documents'),
    path('hr/assign-laptop/<int:onboarding_id>/', views.hr_assign_laptop, name='hr_assign_laptop'),
    path('hr/complete/<int:onboarding_id>/', views.hr_complete_onboarding, name='hr_complete_onboarding'),


    path('',views.allonboardingstatus,name='allonboardingstatus')
]