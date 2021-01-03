from django.urls import path
from django.views.decorators.csrf import csrf_exempt


from .views import index, addExpense, editExpense, deleteExpense, searchExpense, expenseCategorySummary, expenseSummary, exportExpenseCsv, exportExpenseExcel, exportExpensePdf, expense

urlpatterns = [
    path('', index, name='home'),
    path('expenses/', expense, name='expenses'),
    path('add_expense/', addExpense, name='add-expense'),
    path('edit/<int:expense_id>', editExpense, name='edit-expense'),
    path('delete/<int:expense_id>', deleteExpense, name='delete-expense'),
    path('search_expense', csrf_exempt(searchExpense), name='search-expense'),
    path('expense_summary', expenseSummary, name='expense-summary'),
    path('expense_category', expenseCategorySummary, name='expense-category'),
    path('expense_csv', exportExpenseCsv, name='expense-csv'),
    path('expense_excel', exportExpenseExcel, name='expense-excel'),
    path('expense_pdf', exportExpensePdf, name='expense-pdf'),
]
