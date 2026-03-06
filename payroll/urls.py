from django.urls import path
from .views import (
    delete_payroll_record,
    delete_staff,
    export_payroll_excel,
    export_payroll_pdf,
    generate_p9,
    generate_payslip,
    payroll_overview,
    staff_management,
)

urlpatterns = [
    path('', payroll_overview, name='payroll_overview'),
    path('staff/', staff_management, name='staff_management'),
    path('staff/<int:staff_id>/delete/', delete_staff, name='delete_staff'),
    path('payslip/<int:record_id>/', generate_payslip, name='generate_payslip'),
    path('p9/<int:record_id>/', generate_p9, name='generate_p9'),
    path('record/<int:record_id>/delete/', delete_payroll_record, name='delete_payroll_record'),
    path('export/pdf/', export_payroll_pdf, name='export_payroll_pdf'),
    path('export/excel/', export_payroll_excel, name='export_payroll_excel'),
]
