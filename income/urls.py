from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import index, addIncome, editIncome, deleteIncome, searchIncome, incomeSourceSummary, incomeSummary,exportIncomeCsv, exportIncomeExcel, exportIncomePdf

urlpatterns = [
    path('', index, name = 'income' ),
    path('add_income/', addIncome, name='add-income'),
    path('edit/<int:income_id>', editIncome, name='edit-income'),
    path('delete/<int:income_id>', deleteIncome, name='delete-income'),
    path('search_income', csrf_exempt(searchIncome), name='search-income'),
    path('income_summary', incomeSummary, name='income-summary'),
    path('income_source', incomeSourceSummary, name='income-source'),
    path('income_csv', exportIncomeCsv, name='income-csv'),
    path('income_excel', exportIncomeExcel, name='income-excel'),
    path('income_pdf', exportIncomePdf, name='income-pdf'),
    
    
]
