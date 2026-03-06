from django.contrib import admin
from .models import Expenditure, FeePayment, FeePaymentAllocation, FeeStructure

admin.site.register(FeeStructure)
admin.site.register(FeePayment)
admin.site.register(FeePaymentAllocation)
admin.site.register(Expenditure)
