from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views


from accounts.views import LoginView, regiterUser, UsernameValidationView, EmailValidationView,userLogout
urlpatterns = [

    path('validate_username',csrf_exempt(UsernameValidationView.as_view()), name = 'username-validate'),
    path('validate_email',csrf_exempt(EmailValidationView.as_view()), name = 'email-validate'),
    path('register/', regiterUser, name = 'register'),
    path('login/', LoginView, name = 'login'),
    path('logout', userLogout, name = 'logout'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html'), name = 'password_reset'),
    path('reset_email_sent/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name = 'password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name = 'password_reset_confirm'),
    path('reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name = 'password_reset_complete'),
]