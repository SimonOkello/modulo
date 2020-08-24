from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import index, addIncome, editIncome, deleteIncome, searchIncome

urlpatterns = [
    path('', index, name = 'income' ),
    path('add_income/', addIncome, name='add-income'),
    path('edit/<int:income_id>', editIncome, name='edit-income'),
    path('delete/<int:income_id>', deleteIncome, name='delete-income'),
    path('search_income', csrf_exempt(searchIncome), name='search-income'),
    
]
