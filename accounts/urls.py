from django.urls import path


from accounts.views import LoginView, Register

urlpatterns = [

    # path('login/', LoginView.as_view(), name = 'login'),
    path('register/', Register.as_view(), name = 'register')
]