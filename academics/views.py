from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

def is_teacher(user):
    return user.groups.filter(name='Teachers').exists()

@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    return render(request, 'academics/teacher_dashboard.html')
