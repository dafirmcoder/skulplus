from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Sum
from schools.models import School


class Staff(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    role = models.CharField(max_length=100)
    employee_number = models.CharField(max_length=50, blank=True)
    national_id = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    kra_pin = models.CharField(max_length=20)
    nssf_number = models.CharField(max_length=30)
    nhif_number = models.CharField(max_length=30, blank=True)
    employment_type = models.CharField(
        max_length=20,
        choices=(
            ('PERMANENT', 'Permanent'),
            ('CONTRACT', 'Contract'),
            ('PART_TIME', 'Part Time'),
            ('CASUAL', 'Casual'),
        ),
        default='PERMANENT',
    )
    employment_date = models.DateField(default=date.today)
    bank_name = models.CharField(max_length=100, blank=True)
    bank_account_number = models.CharField(max_length=50, blank=True)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_teacher = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['full_name', 'id']

    def __str__(self):
        return self.full_name


class PayrollRecord(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)
    year = models.IntegerField()
    days_worked = models.PositiveSmallIntegerField(default=30, validators=[MinValueValidator(0), MaxValueValidator(30)])
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paye_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    nssf_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    nhif_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    housing_levy_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Other deductions
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-year', '-id']

    def total_allowances(self):
        allowance_total = self.allowances_rows.aggregate(total=Sum('amount')).get('total')
        return allowance_total if allowance_total is not None else (self.allowances or 0)

    def payable_basic_salary(self):
        try:
            return (self.staff.basic_salary * self.days_worked) / 30
        except Exception:
            return self.staff.basic_salary or 0

    def total_deductions(self):
        other_deductions_total = self.other_deductions.aggregate(total=Sum('amount')).get('total')
        other_total = other_deductions_total if other_deductions_total is not None else (self.deductions or 0)
        return (
            (self.paye_deduction or 0)
            + (self.nssf_deduction or 0)
            + (self.nhif_deduction or 0)
            + (self.housing_levy_deduction or 0)
            + other_total
        )

    def net_salary(self):
        return self.payable_basic_salary() + self.total_allowances() - self.total_deductions()

    def __str__(self):
        return f"{self.staff.full_name} - {self.month} {self.year}"


class PayrollOtherDeduction(models.Model):
    payroll_record = models.ForeignKey(PayrollRecord, on_delete=models.CASCADE, related_name='other_deductions')
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.name} ({self.amount})"


class PayrollAllowance(models.Model):
    payroll_record = models.ForeignKey(PayrollRecord, on_delete=models.CASCADE, related_name='allowances_rows')
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.name} ({self.amount})"
