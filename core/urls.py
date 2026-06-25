from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from .forms import EmailAuthenticationForm
from .views import health

urlpatterns = [
    path('', include('accounts.urls')),
    path('', include('clients.urls')),
    path('', include('insurers.urls')),
    path('', include('policies.urls')),
    path('', include('claims.urls')),
    path('', include('renewals.urls')),
    path('', include('attachments.urls')),
    path('', include('crm.urls')),
    path('', include('agents.urls')),
    path('', include('commissions.urls')),
    path('', include('dashboard.urls')),
    path('', include('reports.urls')),
    path('', include('ai.urls')),
    path('health/', health, name='health'),
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(
            authentication_form=EmailAuthenticationForm,
            template_name='registration/login.html',
        ),
        name='login',
    ),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path(
        'accounts/password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt',
        ),
        name='password_reset',
    ),
    path(
        'accounts/password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
        name='password_reset_done',
    ),
    path(
        'accounts/reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
        name='password_reset_confirm',
    ),
    path(
        'accounts/reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
        name='password_reset_complete',
    ),
    path('admin/', admin.site.urls),
]
