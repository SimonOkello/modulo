from django.urls import path


from . import views

urlpatterns = [
    path('', views.profileSettings, name='settings'),
    path('user-profile/', views.userProfile, name='user-profile'),
    path('user-preference/', views.userPreferences, name='user-preference'),
    path('category-setting/', views.expenseCategory, name='category-setting'),
    path('edit-category/<int:category_id>/',
         views.editCategory, name='edit-category'),
    path('delete-category/<int:item_id>/', views.deleteCategory, name="delete-category"),
    path('change-password/', views.changePassword, name='change-password'),
    path('delete-account/', views.deleteAccount, name='delete-account'),

]
