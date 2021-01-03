from django.shortcuts import render, redirect, get_object_or_404
import os
import json
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import userSetting
from expenses.models import Category


@login_required(login_url='/auth/login/')
def profileSettings(request):
    context = {}
    return render(request, 'usersettings/settings.html', context)


@login_required(login_url='/auth/login/')
def userProfile(request):
    context = {}
    return render(request, 'usersettings/profile.html', context)


@login_required(login_url='/auth/login/')
def userPreferences(request):
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

        return render(request, 'usersettings/preferences.html', {'currencies': currency_data, 'user_settings': user_settings})
    else:
        currency = request.POST.get('currency')
        if user_settings_exists:
            user_settings.currency = currency
            user_settings.save()
        else:
            userSetting.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Changes saved!')
        return redirect('user-preference')


@login_required(login_url='/auth/login/')
def expenseCategory(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        notes = request.POST.get('notes')
        Category.objects.create(
            name=name, notes=notes
        )
    else:
        categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'usersettings/expense-category.html', context)


@login_required(login_url='/auth/login/')
def editCategory(request, category_id):
    obj = get_object_or_404(Category, pk=category_id)
    context = {'obj': obj}
    if request.method == 'POST':
        name = request.POST.get('name')
        notes = request.POST.get('notes')
        if not name:
            messages.error(request, 'Name is required')
            return render(request, 'usersettings/edit-category.html', context)
        if not notes:
            messages.error(request, 'Description is required')
            return render(request, 'usersettings/edit-category.html', context)
        obj.name = name
        obj.notes = notes
        obj.save()
        messages.success(request, 'An category was updated successfully')
        return redirect('category-setting')
    return render(request, 'usersettings/edit-category.html', context)


@login_required(login_url='/auth/login/')
def deleteCategory(request, item_id):
    obj = get_object_or_404(Category, pk=item_id)
    obj.delete()
    return redirect('category-setting')


@login_required(login_url='/auth/login/')
def changePassword(request):
    context = {}
    return render(request, 'usersettings/change-password.html', context)


@login_required(login_url='/auth/login/')
def deleteAccount(request):
    context = {}
    return render(request, 'usersettings/delete-account.html', context)
