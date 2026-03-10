from django import forms
from .models import Teacher, Student, Announcement, ClassRoom, Subject, Stream, EducationLevel
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
    cambridge_grading_system = forms.ChoiceField(
        choices=School.CAMBRIDGE_GRADING_CHOICES,
        label='Cambridge Grading',
        required=False,
    )
    school_category = forms.ChoiceField(choices=School.SCHOOL_CATEGORY_CHOICES, label='School Category')
    address = forms.CharField(widget=forms.Textarea, required=False)
    phone = forms.CharField(max_length=50, required=False)
    school_email = forms.EmailField(required=True)

    # Headteacher fields
    head_full_name = forms.CharField(max_length=255, label='Headteacher Full Name')
    head_email = forms.EmailField(label='Headteacher Email')
    head_password = forms.CharField(widget=forms.PasswordInput, label='Password')
    head_phone = forms.CharField(max_length=50, required=False)

    def clean_school_name(self):
        name = (self.cleaned_data.get('school_name') or '').strip()
        if School.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError('A school with that name already exists.')
        return name

    def clean_school_email(self):
        email = (self.cleaned_data.get('school_email') or '').strip().lower()
        if School.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('A school with that email already exists.')
        User = get_user_model()
        if User.objects.filter(username__iexact=email).exists():
            raise forms.ValidationError('That school email is already used by another account.')
        return email

    def clean_head_email(self):
        email = (self.cleaned_data.get('head_email') or '').strip().lower()
        User = get_user_model()
        if User.objects.filter(username__iexact=email).exists():
            raise forms.ValidationError('A user with that email already exists.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        school_type = (cleaned_data.get('school_type') or '').strip().upper()
        if school_type != 'CAMBRIDGE':
            cleaned_data['cambridge_grading_system'] = 'CAMB_9_1'
        school_email = (cleaned_data.get('school_email') or '').strip().lower()
        head_email = (cleaned_data.get('head_email') or '').strip().lower()
        if school_email and head_email and school_email == head_email:
            raise forms.ValidationError(
                'School email and headteacher email must be different. '
                'School email logs into headteacher dashboard; headteacher email logs into teacher dashboard.'
            )
        return cleaned_data


class SchoolSignupForm(forms.Form):
    # School
    school_name = forms.CharField(max_length=255)
    school_type = forms.ChoiceField(choices=[('CAMBRIDGE', 'Cambridge'), ('CBE', 'CBE')])
    cambridge_grading_system = forms.ChoiceField(
        choices=School.CAMBRIDGE_GRADING_CHOICES,
        label='Cambridge Grading',
        required=False,
    )
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
    parent_login_password = forms.CharField(
        label='Parent Login Password',
        required=False,
        disabled=True,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        help_text='Auto-generated as admission number + first name.',
    )

    class Meta:
        model = Student
        fields = [
            'classroom', 'stream', 'first_name', 'last_name', 'date_of_birth', 'gender',
            'admission_number', 'admission_date', 'parent_name', 'parent_phone', 'photo'
        ]

    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)
        super().__init__(*args, **kwargs)

        if school and 'classroom' in self.fields:
            self.fields['classroom'].queryset = ClassRoom.objects.filter(school=school).order_by('name')

        if 'stream' in self.fields:
            stream_qs = Stream.objects.none()
            classroom_id = None
            if self.is_bound:
                classroom_id = self.data.get('classroom')
            elif self.instance and self.instance.classroom_id:
                classroom_id = self.instance.classroom_id

            if classroom_id:
                stream_qs = Stream.objects.filter(classroom_id=classroom_id)
                if school:
                    stream_qs = stream_qs.filter(classroom__school=school)
            elif school:
                stream_qs = Stream.objects.filter(classroom__school=school).none()
            self.fields['stream'].queryset = stream_qs.order_by('name')

        desired_order = [
            'classroom', 'stream', 'first_name', 'last_name', 'date_of_birth', 'gender',
            'admission_number', 'admission_date', 'parent_name', 'parent_phone',
            'parent_login_password', 'photo'
        ]
        self.order_fields(desired_order)

        admission = ''
        first_name = ''
        if self.is_bound:
            admission = (self.data.get('admission_number') or '').strip()
            first_name = (self.data.get('first_name') or '').strip()
        elif self.instance:
            admission = (self.instance.admission_number or '').strip()
            first_name = (self.instance.first_name or '').strip()
        self.fields['parent_login_password'].initial = f'{admission}{first_name}'

    def clean_stream(self):
        stream = self.cleaned_data.get('stream')
        classroom = self.cleaned_data.get('classroom')
        if stream and classroom and stream.classroom_id != classroom.id:
            raise forms.ValidationError('Selected stream does not belong to the selected class.')
        return stream


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
        school = kwargs.pop('school', None)
        super().__init__(*args, **kwargs)
        if 'section' in self.fields:
            self.fields['section'].label = 'Stream'
        if 'class_teacher' in self.fields:
            if school:
                self.fields['class_teacher'].queryset = Teacher.objects.filter(
                    school=school
                ).select_related('user').order_by('user__first_name', 'user__last_name')
            else:
                self.fields['class_teacher'].queryset = Teacher.objects.none()


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['code', 'name', 'short_name', 'subject_category', 'education_level']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. MATH101'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mathematics'}),
            'short_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Math'}),
            'subject_category': forms.Select(attrs={'class': 'form-control'}),
            'education_level': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)
        super().__init__(*args, **kwargs)
        if 'education_level' in self.fields:
            qs = EducationLevel.objects.all().order_by('name')
            if school and getattr(school, 'school_type', '') == 'CAMBRIDGE':
                qs = qs.filter(name__in=['Kindergarten', 'Lower Primary', 'Upper Primary', 'Lower Secondary', 'Upper Secondary (IGCSE)', 'A Level'])
            self.fields['education_level'].queryset = qs
            self.fields['education_level'].required = True


class SchoolDetailsForm(forms.ModelForm):
    class Meta:
        model = School
        fields = [
            'name',
            'motto',
            'school_category',
            'cambridge_grading_system',
            'cambridge_show_ranking',
            'address',
            'phone',
            'email',
            'logo',
            'stamp',
            'head_signature',
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'motto': forms.TextInput(attrs={'class': 'form-control'}),
            'school_category': forms.Select(attrs={'class': 'form-control'}),
            'cambridge_grading_system': forms.Select(attrs={'class': 'form-control'}),
            'cambridge_show_ranking': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
