from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.db.models import Sum
import tempfile
import datetime
import json
import csv
import xlwt


# Create your views here.
from .models import Category, Expense
from income.models import Income
from usersettings.models import userSetting


@login_required(login_url='/auth/login/')
def index(request):
    expenses = Expense.objects.filter(owner=request.user)[:5]
    incomes = Income.objects.filter(owner=request.user)[:5]
    sum_of_expenses = Expense.objects.all().aggregate(Sum('amount'))[
        'amount__sum'] or 0.00
    sum_of_income = Income.objects.all().aggregate(Sum('amount'))[
        'amount__sum'] or 0.00
    currency = userSetting.objects.get(user=request.user).currency
    context = {'expenses': expenses, 'incomes': incomes, 'currency': currency,
               'sum_of_expenses': sum_of_expenses, 'sum_of_income': sum_of_income}
    return render(request, 'expenses/index.html', context)


@login_required(login_url='/auth/login/')
def expense(request):
    expenses = Expense.objects.filter(owner=request.user)
    currency = userSetting.objects.get(user=request.user).currency
    context = {'expenses': expenses, 'currency': currency}
    return render(request, 'expenses/expenses.html', context)


@login_required(login_url='/auth/login/')
def addExpense(request):
    categories = Category.objects.all()
    context = {'categories': categories, 'values': request.POST}
    if request.method == 'GET':

        return render(request, 'expenses/add-expense.html', context)

    if request.method == 'POST':
        category = request.POST.get('category')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        date = request.POST.get('date')

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/add-expense.html', context)
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add-expense.html', context)

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'expenses/add-expense.html', context)

        Expense.objects.create(owner=request.user, category=category,
                               description=description, amount=amount, date=date)
        messages.success(request, 'An expense was created successfully')
        return redirect('expenses')
    return render(request, 'expenses/add-expense.html', context)


@login_required(login_url='/auth/login/')
def editExpense(request, expense_id):
    categories = Category.objects.all()
    expense = get_object_or_404(Expense, pk=expense_id)
    context = {'expense': expense, 'values': expense, 'categories': categories}
    if request.method == 'POST':
        category = request.POST.get('category')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        date = request.POST.get('date')

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/edit-expense.html', context)
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)

        expense.owner = request.user
        expense.category = category
        expense.description = description
        expense.amount = amount
        expense.date = date
        expense.save()
        messages.success(request, 'An expense was updated successfully')
        return redirect('expenses')

    return render(request, 'expenses/edit-expense.html', context)


@login_required(login_url='/auth/login/')
def deleteExpense(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    expense.delete()
    return redirect('expenses')


def searchExpense(request):
    if request.method == 'POST':
        search_string = json.loads(request.body).get('searchText')

        expenses = Expense.objects.filter(amount__istartswith=search_string, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_string, owner=request.user) | Expense.objects.filter(
                description__icontains=search_string, owner=request.user) | Expense.objects.filter(
                    category__icontains=search_string, owner=request.user)

        data = expenses.values()
        return JsonResponse(list(data), safe=False)

# EXPENSE SUMMARY


def expenseCategorySummary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=180)
    expenses = Expense.objects.filter(owner=request.user,
                                      date__gte=six_months_ago, date__lte=todays_date)
    final_representation = {}

    def get_category(expense):
        return expense.category

    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):

        amount = 0
        filtered_by_category = expenses.filter(category=category)
        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            final_representation[y] = get_expense_category_amount(y)
    return JsonResponse({'expense_category_data': final_representation}, safe=False)


def expenseSummary(request):
    return render(request, 'expenses/expense_summary.html', {})


# REPORTS
def exportExpenseCsv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses ' + \
        str(datetime.datetime.now()) + '.csv'
    writer = csv.writer(response)
    writer.writerow(['Category', 'Description', 'Amount', 'Date'])

    expenses = Expense.objects.filter(owner=request.user)

    for expense in expenses:
        writer.writerow([expense.category, expense.description,
                         expense.amount, expense.date])

    return response


def exportExpenseExcel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Expenses ' + \
        str(datetime.datetime.now()) + '.xlsx'

    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('Expenses')
    row_number = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Category', 'Description', 'Amount', 'Date']

    for col_num in range(len(columns)):
        worksheet.write(row_number, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = Expense.objects.filter(owner=request.user).values_list(
        'category', 'description', 'amount', 'date')

    for row in rows:
        row_number += 1
        for col_num in range(len(row)):
            worksheet.write(row_number, col_num, str(row[col_num]), font_style)

    workbook.save(response)

    return response


def exportExpensePdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=Expenses ' + \
        str(datetime.datetime.now()) + '.pdf'

    response['Content-Transfer-Encoding'] = 'binary'

    expenses = Expense.objects.filter(owner=request.user)
    sum = expenses.aggregate(Sum('amount'))

    html_string = render_to_string(
        'expenses/pdf_printout.html', {'expenses': expenses, 'total': sum['amount__sum']})

    html = HTML(string=html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    return response
