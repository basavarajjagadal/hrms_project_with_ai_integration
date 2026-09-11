from django.contrib import admin

# Register your models here.

from .models import Onboarding,IDProof,BankDetails,Verification,LaptopAllocation

admin.site.register(Onboarding)
admin.site.register(IDProof)
admin.site.register(BankDetails)
admin.site.register(Verification)
admin.site.register(LaptopAllocation)