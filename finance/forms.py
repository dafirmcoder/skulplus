from django import forms

from .models import Expenditure, FeePayment

class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeePayment
        fields = ['student', 'term', 'year', 'amount_paid', 'payment_method']


class ExpenditureForm(forms.ModelForm):
    class Meta:
        model = Expenditure
        fields = [
            'date',
            'item',
            'amount',
            'quantity',
            'vote_head',
            'payment_method',
            'receipt_invoice_no',
            'evidence_document',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_evidence_document(self):
        file = self.cleaned_data.get('evidence_document')
        if not file:
            return file

        name = (file.name or '').lower()
        allowed = ('.pdf', '.png', '.jpg', '.jpeg', '.webp')
        if not name.endswith(allowed):
            raise forms.ValidationError('Evidence document must be PDF or image (PNG/JPG/JPEG/WEBP).')
        return file
