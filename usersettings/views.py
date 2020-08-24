from django.shortcuts import render, redirect
import os
import json
from django.conf import settings
from django.contrib import messages

# Create your views here.
from .models import userSetting


def index(request):
    user_settings_exists = userSetting.objects.filter(
        user=request.user).exists()
    user_settings = None
    if user_settings_exists:
        user_settings = userSetting.objects.get(user=request.user)

    if request.method == 'GET':
        currency_data = []
        file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

            for k, v in data.items():
                currency_data.append({'name': k, 'value': v})

        return render(request, 'usersettings/index.html', {'currencies': currency_data, 'user_settings':user_settings})
    else:
        currency = request.POST.get('currency')
        if user_settings_exists:
            user_settings.currency = currency
            user_settings.save()
        else:
            userSetting.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Changes saved!')
        return redirect('home')
