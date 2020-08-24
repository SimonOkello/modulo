from django.urls import path
from django.views.decorators.csrf import csrf_exempt


from .views import index, addExpense, editExpense, deleteExpense, searchExpense, expenseCategorySummary, expenseSummary, exportCsv, exportExcel, exportPdf

urlpatterns = [
    path('', index, name='home'),
    path('add_expense/', addExpense, name='add-expense'),
    path('edit/<int:expense_id>', editExpense, name='edit-expense'),
    path('delete/<int:expense_id>', deleteExpense, name='delete-expense'),
    path('search_expense', csrf_exempt(searchExpense), name='search-expense'),
    path('expense_category', expenseCategorySummary, name='expense-category'),
    path('expense_summary', expenseSummary, name='expense-summary'),
    path('csv', exportCsv, name='export-csv'),
    path('excel', exportExcel, name='export-excel'),
    path('pdf', exportPdf, name='export-pdf'),
]
