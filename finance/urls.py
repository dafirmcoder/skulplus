from django.urls import path
from .views import balance_report, expenditure_evidence, expenditure_report, fee_receipt, fee_structure, model_reports

urlpatterns = [
    path('balance-report/', balance_report, name='balance_report'),
    path('model-reports/', model_reports, name='model_reports'),
    path('fee-structure/', fee_structure, name='fee_structure'),
    path('expenditure/', expenditure_report, name='expenditure'),
    path('expenditure/<int:expenditure_id>/evidence/', expenditure_evidence, name='expenditure_evidence'),
    path('receipt/<int:payment_id>/', fee_receipt, name='fee_receipt'),
]
