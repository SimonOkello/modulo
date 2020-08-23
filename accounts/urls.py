from django.urls import path
from django.views.decorators.csrf import csrf_exempt


from accounts.views import LoginView, regiterUser, UsernameValidationView, EmailValidationView,userLogout
urlpatterns = [

    path('validate_username',csrf_exempt(UsernameValidationView.as_view()), name = 'username-validate'),
    path('validate_email',csrf_exempt(EmailValidationView.as_view()), name = 'email-validate'),
    path('register/', regiterUser, name = 'register'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('logout', userLogout, name = 'logout'),
]