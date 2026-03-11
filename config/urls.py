"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from finance.views import add_payment, add_payment_meta, send_fee_reminders
from schools import views as schools_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', schools_views.logout_view, name='logout'),
    path('accounts/logout/', schools_views.logout_view, name='accounts_logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('finance/', include('finance.urls')),
    path('add-payment/', add_payment, name='add_payment'),
    path('add-payment/meta/', add_payment_meta, name='add_payment_meta'),
    path('payroll/', include('payroll.urls')),
    path('send-reminders/', send_fee_reminders, name='send_fee_reminders'),
    path('academics/', include('academics.urls')),
    path('school/', include('schools.urls')),
    # Landing/home page
    path('login/', schools_views.login_view, name='login'),
    path('signup/', schools_views.signup_modal_redirect, name='signup'),
    path('post-login/', schools_views.post_login_redirect, name='post_login'),
    path('features/academics/', schools_views.features_academics, name='feature_academics'),
    path('features/finance/', schools_views.features_finance, name='feature_finance'),
    path('features/payroll/', schools_views.features_payroll, name='feature_payroll'),
    path('features/parents/', schools_views.features_parents, name='feature_parents'),
    path('resources/', schools_views.resources_select, name='resources_select'),
    path('resources/<str:curriculum>/', schools_views.resources, name='resources'),
    path('', schools_views.landing, name='landing'),

   
]
from django.conf import settings
from django.conf.urls.static import static

if settings.MEDIA_URL:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
