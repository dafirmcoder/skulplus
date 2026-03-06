from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import PayrollAllowance, PayrollOtherDeduction, PayrollRecord, Staff


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'role', 'school', 'kra_pin', 'nssf_number', 'basic_salary', 'is_active')
    search_fields = ('full_name', 'role', 'kra_pin', 'nssf_number', 'employee_number')
    list_filter = ('school', 'employment_type', 'is_active')


@admin.register(PayrollRecord)
class PayrollRecordAdmin(admin.ModelAdmin):
    list_display = ('staff', 'month', 'year', 'days_worked', 'total_deductions', 'net_salary', 'payslip_link')

    def payslip_link(self, obj):
        url = reverse('generate_payslip', args=[obj.id])
        return format_html('<a class="button" href="{}" target="_blank">Download Payslip</a>', url)

    payslip_link.short_description = "Payslip"


@admin.register(PayrollOtherDeduction)
class PayrollOtherDeductionAdmin(admin.ModelAdmin):
    list_display = ('payroll_record', 'name', 'amount')
    search_fields = ('name', 'payroll_record__staff__full_name')


@admin.register(PayrollAllowance)
class PayrollAllowanceAdmin(admin.ModelAdmin):
    list_display = ('payroll_record', 'name', 'amount')
    search_fields = ('name', 'payroll_record__staff__full_name')
