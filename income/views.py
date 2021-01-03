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
from .models import Source, Income
from usersettings.models import userSetting


@login_required(login_url='/auth/login/')
def index(request):
    incomes = Income.objects.filter(owner=request.user)
    currency = userSetting.objects.get(user=request.user).currency
    context = {'incomes': incomes,'currency': currency}
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


# INCOME SUMMARY
def incomeSourceSummary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=180)
    incomes = Income.objects.filter(owner=request.user,
                                      date__gte=six_months_ago, date__lte=todays_date)
    final_representation = {}

    def get_source(income):
        return income.source

    source_list = list(set(map(get_source, incomes)))

    def get_income_source_amount(source):

        amount = 0
        filtered_by_source = incomes.filter(source=source)
        for item in filtered_by_source:
            amount += item.amount
        return amount

    for x in incomes:
        for y in source_list:
            final_representation[y] = get_income_source_amount(y)
    return JsonResponse({'income_source_data': final_representation}, safe=False)


def incomeSummary(request):
    return render(request, 'income/income_summary.html', {})

# REPORTS
def exportIncomeCsv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Income ' + \
        str(datetime.datetime.now()) + '.csv'
    writer = csv.writer(response)
    writer.writerow(['Source', 'Description', 'Amount', 'Date'])

    incomes = Income.objects.filter(owner=request.user)

    for income in incomes:
        writer.writerow([income.source, income.description,
                         income.amount, income.date])

    return response


def exportIncomeExcel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Income ' + \
        str(datetime.datetime.now()) + '.xlsx'

    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('Income')
    row_number = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Source', 'Description', 'Amount', 'Date']

    for col_num in range(len(columns)):
        worksheet.write(row_number, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = Income.objects.filter(owner=request.user).values_list(
        'source', 'description', 'amount', 'date')

    for row in rows:
        row_number += 1
        for col_num in range(len(row)):
            worksheet.write(row_number, col_num, str(row[col_num]), font_style)

    workbook.save(response)

    return response


def exportIncomePdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=Income ' + \
        str(datetime.datetime.now()) + '.pdf'

    response['Content-Transfer-Encoding'] = 'binary'

    incomes = Income.objects.filter(owner=request.user)
    sum = incomes.aggregate(Sum('amount'))

    html_string = render_to_string(
        'income/pdf_printout.html', {'incomes': incomes, 'total': sum['amount__sum']})

    html = HTML(string=html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    return response
