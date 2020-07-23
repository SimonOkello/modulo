from django.urls import path
from django.views.decorators.csrf import csrf_exempt


from accounts.views import LoginView, Register, UsernameValidationView

urlpatterns = [

    path('validate_username',csrf_exempt(UsernameValidationView.as_view()), name = 'username-validate'),
    path('register/', Register.as_view(), name = 'register')
]