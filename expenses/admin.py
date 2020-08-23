from django.contrib import admin

# Register your models here.
from .models import Expense, Category
from usersettings.models import userSetting


admin.site.register(Expense)
admin.site.register(Category)
admin.site.register(userSetting)