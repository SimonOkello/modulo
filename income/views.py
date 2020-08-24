from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse

# Create your views here.
from .models import Source, Income
from usersettings.models import userSetting


@login_required(login_url='/auth/login/')
def index(request):
    sources = Source.objects.all()
    incomes = Income.objects.filter(owner=request.user)
    currency = userSetting.objects.get(user=request.user).currency
    paginator = Paginator(incomes, 5)
    page_number = request.GET.get('page', 1)
    page_obj = Paginator.get_page(paginator, page_number)
    context = {'sources': sources,
               'incomes': incomes, 'page_obj': page_obj, 'currency':currency}
    return render(request, 'income/index.html', context)


@login_required(login_url='/auth/login/')
def addIncome(request):
    sources = Source.objects.all()
    context = {'sources': sources, 'values': request.POST}
    if request.method == 'GET':

        return render(request, 'income/add_income.html', context)

    if request.method == 'POST':
        source = request.POST.get('source')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        date = request.POST.get('date')

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/add_income.html', context)
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html', context)

        Income.objects.create(owner=request.user, source=source,
                               description=description, amount=amount, date=date)
        messages.success(request, 'Income was created successfully')
        return redirect('income')
    return render(request, 'income/add_income.html', context)


@login_required(login_url='/auth/login/')
def editIncome(request, income_id):
    sources = Source.objects.all()
    income = get_object_or_404(Income, pk=income_id)
    sources = Source.objects.all()
    context = {'income': income, 'values': income, 'sources': sources}
    if request.method == 'POST':
        source = request.POST.get('source')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        date = request.POST.get('date')

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/edit_income.html', context)
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/edit_income.html', context)

        income.owner = request.user
        income.source = source
        income.description = description
        income.amount = amount
        income.date = date
        income.save()
        messages.success(request, 'Income was updated successfully')
        return redirect('income')

    return render(request, 'income/edit_income.html', context)


@login_required(login_url='/auth/login/')
def deleteIncome(request, income_id):
    income = get_object_or_404(Income, pk=income_id)
    income.delete()
    messages.success(request, 'Income deleted!')
    return redirect('income')


def searchIncome(request):
    if request.method == 'POST':
        search_string = json.loads(request.body).get('searchText')

        incomes = Income.objects.filter(amount__istartswith=search_string, owner=request.user) | Income.objects.filter(
            date__istartswith=search_string, owner=request.user) | Income.objects.filter(
                description__icontains=search_string, owner=request.user) | Income.objects.filter(
                    source__icontains=search_string, owner=request.user)

        data = incomes.values()
        return JsonResponse(list(data), safe=False)
