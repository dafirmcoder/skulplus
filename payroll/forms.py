from django import forms
from decimal import Decimal

from .models import PayrollRecord, Staff


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = [
            'full_name',
            'role',
            'employee_number',
            'national_id',
            'phone',
            'email',
            'kra_pin',
            'nssf_number',
            'nhif_number',
            'employment_type',
            'employment_date',
            'bank_name',
            'bank_account_number',
            'basic_salary',
            'is_teacher',
            'is_active',
        ]
        widgets = {
            'employment_date': forms.DateInput(attrs={'type': 'date'}),
        }


class PayrollRecordForm(forms.ModelForm):
    MONTH_CHOICES = [
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    ]
    PERCENT_CHOICES = [
        ('0', '0%'),
        ('1', '1%'),
        ('1.5', '1.5%'),
        ('2', '2%'),
        ('2.5', '2.5%'),
        ('3', '3%'),
        ('5', '5%'),
        ('10', '10%'),
        ('15', '15%'),
        ('20', '20%'),
        ('25', '25%'),
        ('30', '30%'),
    ]

    month = forms.ChoiceField(choices=MONTH_CHOICES)
    days_worked = forms.IntegerField(min_value=0, max_value=30, initial=30)
    paye_rate = forms.ChoiceField(choices=PERCENT_CHOICES, initial='0')
    nssf_rate = forms.ChoiceField(choices=PERCENT_CHOICES, initial='0')
    nhif_rate = forms.ChoiceField(choices=PERCENT_CHOICES, initial='0')
    housing_levy_rate = forms.ChoiceField(choices=PERCENT_CHOICES, initial='0')

    class Meta:
        model = PayrollRecord
        fields = [
            'month',
            'year',
            'days_worked',
        ]

    def apply_statutory_values(self, record, staff):
        basic_salary = getattr(staff, 'basic_salary', Decimal('0')) or Decimal('0')
        days_worked = Decimal(self.cleaned_data.get('days_worked') or 0)
        payable_basic_salary = (basic_salary * days_worked) / Decimal('30')

        paye_rate = Decimal(self.cleaned_data.get('paye_rate') or '0')
        nssf_rate = Decimal(self.cleaned_data.get('nssf_rate') or '0')
        nhif_rate = Decimal(self.cleaned_data.get('nhif_rate') or '0')
        housing_levy_rate = Decimal(self.cleaned_data.get('housing_levy_rate') or '0')

        record.days_worked = int(days_worked)
        record.paye_deduction = (payable_basic_salary * paye_rate) / Decimal('100')
        record.nssf_deduction = (payable_basic_salary * nssf_rate) / Decimal('100')
        record.nhif_deduction = (payable_basic_salary * nhif_rate) / Decimal('100')
        record.housing_levy_deduction = (payable_basic_salary * housing_levy_rate) / Decimal('100')
        record.allowances = Decimal('0')
        record.deductions = Decimal('0')
