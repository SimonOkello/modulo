from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
import json
from validate_email import validate_email
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from .forms import CreateUserForm


class UsernameValidationView(View):

    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric.'}, status=400)
        return JsonResponse({'username_valid': True})

        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Username is taken'}, status=409)
        return JsonResponse({'username_valid': True})


class EmailValidationView(View):

    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'The email is invalid.'}, status=400)
        return JsonResponse({'email_valid': True})

        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Email is taken'}, status=409)
        return JsonResponse({'email_valid': True})


class LoginView(View):

    def get(self, request):
        return render(request, 'accounts/login.html', {})

    def post(self, request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            if username and password:

                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Incorrect Credentials!')
                    return render(request, 'accounts/login.html', {})

            messages.error(request, 'Please fill out all fields')
            return render(request, 'accounts/login.html', {})
        return render(request, 'accounts/login.html', {})


def regiterUser(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    return render(request, 'accounts/register.html', {'form': form})

def userLogout(request):
    logout(request)
    return redirect('login')