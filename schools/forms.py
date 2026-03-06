from django import forms
from .models import Teacher, Student, Announcement, ClassRoom, Subject
from .models import School
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class SignUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email")


class SchoolRegistrationForm(forms.Form):
    # School fields
    school_name = forms.CharField(max_length=255, label='School Name')
    school_type = forms.ChoiceField(choices=(('CAMBRIDGE', 'Cambridge'), ('CBE', 'CBE')))
    school_category = forms.ChoiceField(choices=School.SCHOOL_CATEGORY_CHOICES, label='School Category')
    address = forms.CharField(widget=forms.Textarea, required=False)
    phone = forms.CharField(max_length=50, required=False)
    school_email = forms.EmailField(required=False)

    # Headteacher fields
    head_full_name = forms.CharField(max_length=255, label='Headteacher Full Name')
    head_email = forms.EmailField(label='Headteacher Email')
    head_password = forms.CharField(widget=forms.PasswordInput, label='Password')
    head_phone = forms.CharField(max_length=50, required=False)

    def clean_head_email(self):
        email = self.cleaned_data.get('head_email')
        User = get_user_model()
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError('A user with that email already exists.')
        return email


class SchoolSignupForm(forms.Form):
    # School
    school_name = forms.CharField(max_length=255)
    school_type = forms.ChoiceField(choices=[('CAMBRIDGE', 'Cambridge'), ('CBE', 'CBE')])
    school_category = forms.ChoiceField(choices=School.SCHOOL_CATEGORY_CHOICES, label='School Category')
    school_email = forms.EmailField()
    phone = forms.CharField(max_length=50)

    # Headteacher
    head_full_name = forms.CharField(max_length=200)
    head_email = forms.EmailField()
    head_password = forms.CharField(widget=forms.PasswordInput)

    def clean_head_email(self):
        email = self.cleaned_data.get('head_email')
        User = get_user_model()
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError('A user with that email already exists.')
        return email


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['user', 'is_class_teacher']


class NewTeacherForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    is_class_teacher = forms.BooleanField(required=False)


class TeacherAllocationForm(forms.Form):
    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.none(), required=False)
    classes = forms.ModelMultipleChoiceField(queryset=ClassRoom.objects.none(), required=False)

    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)
        super().__init__(*args, **kwargs)
        if school:
            self.fields['subjects'].queryset = Subject.objects.filter(school=school)
            self.fields['classes'].queryset = ClassRoom.objects.filter(school=school)


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'classroom', 'stream', 'first_name', 'last_name', 'date_of_birth', 'gender',
            'admission_number', 'admission_date', 'parent_name', 'parent_phone', 'parent_user', 'photo'
        ]


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'message']


class ClassRoomForm(forms.ModelForm):
    class Meta:
        model = ClassRoom
        fields = ['name', 'section', 'level', 'class_teacher']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Grade 5'}),
            'section': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. East'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'class_teacher': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'section' in self.fields:
            self.fields['section'].label = 'Stream'


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['code', 'name', 'short_name', 'subject_category']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. MATH101'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mathematics'}),
            'short_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Math'}),
            'subject_category': forms.Select(attrs={'class': 'form-control'}),
        }


class SchoolDetailsForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'motto', 'school_category', 'address', 'phone', 'email', 'logo', 'stamp', 'head_signature']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'motto': forms.TextInput(attrs={'class': 'form-control'}),
            'school_category': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
