from django.urls import path


from .views import index
from accounts.views import LoginView

urlpatterns = [
    path('', LoginView.as_view(), name = 'login'),
    path('home', index, name='index'),
    
]