from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse

# Create your views here.
from .models import Category, Expense


@login_required(login_url='/auth/login/')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page', 1)
    page_obj = Paginator.get_page(paginator, page_number)
    context = {'categories': categories,
               'expenses': expenses, 'page_obj': page_obj}
    return render(request, 'expenses/index.html', context)


@login_required(login_url='/auth/login/')
def addExpense(request):
    categories = Category.objects.all()
    context = {'categories': categories, 'values': request.POST}
    if request.method == 'GET':

        return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        category = request.POST.get('category')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        date = request.POST.get('date')

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/add_expense.html', context)
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)

        Expense.objects.create(owner=request.user, category=category,
                               description=description, amount=amount, date=date)
        messages.success(request, 'An expense was created successfully')
        return redirect('home')
    return render(request, 'expenses/add_expense.html', context)


@login_required(login_url='/auth/login/')
def editExpense(request, expense_id):
    categories = Category.objects.all()
    expense = get_object_or_404(Expense, pk=expense_id)
    categories = Category.objects.all()
    context = {'expense': expense, 'values': expense, 'categories': categories}
    if request.method == 'POST':
        category = request.POST.get('category')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        date = request.POST.get('date')

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/edit_expense.html', context)
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit_expense.html', context)

        expense.owner = request.user
        expense.category = category
        expense.description = description
        expense.amount = amount
        expense.date = date
        expense.save()
        messages.success(request, 'An expense was updated successfully')
        return redirect('home')

    return render(request, 'expenses/edit_expense.html', context)


@login_required(login_url='/auth/login/')
def deleteExpense(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    expense.delete()
    return redirect('home')


def searchExpense(request):
    if request.method == 'POST':
        search_string = json.loads(request.body).get('searchText')

        expenses = Expense.objects.filter(amount__istartswith=search_string, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_string, owner=request.user) | Expense.objects.filter(
                description__icontains=search_string, owner=request.user) | Expense.objects.filter(
                    category__icontains=search_string, owner=request.user)

        data = expenses.values()
        return JsonResponse(list(data), safe=False)
