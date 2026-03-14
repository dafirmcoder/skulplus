from django.core.exceptions import ValidationError
from django.db import models

from schools.models import ClassRoom, School, Student


class FeeStructure(models.Model):
    BILLING_MODE_ONCE_YEAR = 'ONCE_YEAR'
    BILLING_MODE_SELECTED_TERMS = 'SELECTED_TERMS'

    BILLING_MODE_CHOICES = (
        (BILLING_MODE_ONCE_YEAR, 'Once a year'),
        (BILLING_MODE_SELECTED_TERMS, 'Selected terms'),
    )

    TERM_CHOICES = (
        ('Term 1', 'Term 1'),
        ('Term 2', 'Term 2'),
        ('Term 3', 'Term 3'),
    )

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='fee_structures')
    vote_head = models.CharField(max_length=120, default='General')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.IntegerField()
    billing_mode = models.CharField(max_length=20, choices=BILLING_MODE_CHOICES, default=BILLING_MODE_SELECTED_TERMS)
    due_term = models.CharField(max_length=20, choices=TERM_CHOICES, blank=True)
    applied_terms = models.JSONField(default=list, blank=True)
    applicable_classes = models.ManyToManyField(ClassRoom, related_name='fee_structures')

    class Meta:
        ordering = ['-year', 'vote_head']

    def clean(self):
        super().clean()

        if self.billing_mode == self.BILLING_MODE_ONCE_YEAR:
            if not self.due_term:
                raise ValidationError({'due_term': 'Choose the term for once-a-year vote head payment.'})
            self.applied_terms = []
            return

        if self.billing_mode == self.BILLING_MODE_SELECTED_TERMS:
            terms = self.applied_terms or []
            valid_terms = {choice[0] for choice in self.TERM_CHOICES}
            if not terms:
                raise ValidationError({'applied_terms': 'Select at least one term.'})
            invalid = [t for t in terms if t not in valid_terms]
            if invalid:
                raise ValidationError({'applied_terms': f'Invalid term selections: {", ".join(invalid)}'})
            self.due_term = ''

    def __str__(self):
        return f'{self.school.name} - {self.vote_head} ({self.year})'


class FeePayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    term = models.CharField(max_length=20)
    year = models.IntegerField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, choices=(
        ('Cash', 'Cash'),
        ('Bank', 'Bank Transfer'),
        ('M-Pesa', 'M-Pesa'),
    ))
    mpesa_code = models.CharField(max_length=120, blank=True, db_index=True)
    bank_slip_no = models.CharField(max_length=120, blank=True, db_index=True)
    cheque_no = models.CharField(max_length=120, blank=True, db_index=True)

    def __str__(self):
        return f'{self.student} - {self.amount_paid}'


class FeePaymentAllocation(models.Model):
    fee_payment = models.ForeignKey(FeePayment, on_delete=models.CASCADE, related_name='allocations')
    allocation_term = models.CharField(max_length=20)
    allocation_year = models.IntegerField()
    vote_head = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['allocation_year', 'allocation_term', 'vote_head', 'id']

    def __str__(self):
        return f'{self.fee_payment_id} - {self.allocation_year} {self.allocation_term} {self.vote_head}: {self.amount}'


class Expenditure(models.Model):
    SOURCE_MANUAL = 'MANUAL'
    SOURCE_PAYROLL = 'PAYROLL'
    SOURCE_CHOICES = (
        (SOURCE_MANUAL, 'Manual'),
        (SOURCE_PAYROLL, 'Payroll'),
    )
    PAYMENT_METHOD_CHOICES = (
        ('Cash', 'Cash'),
        ('Bank Transfer', 'Bank Transfer'),
        ('M-Pesa', 'M-Pesa'),
    )

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='expenditures')
    date = models.DateField()
    item = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    vote_head = models.CharField(max_length=120, default='General')
    receipt_invoice_no = models.CharField(max_length=120, blank=True)
    evidence_document = models.FileField(upload_to='expenditures/evidence/', null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default='Cash')
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default=SOURCE_MANUAL)
    payroll_month = models.CharField(max_length=20, blank=True, default='')
    payroll_year = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-id']

    @property
    def total_value(self):
        return (self.amount or 0) * (self.quantity or 0)

    def __str__(self):
        return f'{self.item} - {self.amount} ({self.date})'


class Budget(models.Model):
    TERM_CHOICES = FeeStructure.TERM_CHOICES

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='budgets')
    vote_head = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    year = models.IntegerField()
    term = models.CharField(max_length=20, choices=TERM_CHOICES, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-year', 'term', 'vote_head', '-id']
        unique_together = ('school', 'year', 'term', 'vote_head')

    def __str__(self):
        term_label = self.term or 'Full Year'
        return f'{self.school.name} {self.year} {term_label} - {self.vote_head}'

