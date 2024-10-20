from django.contrib import admin
from .models import Expense,Category
# Register your models here.


class ToShowAttributesInExpenses(admin.ModelAdmin):
    list_display = ("amount",
                    "date",
                    "description",
                    "owner",
                    "category",)


admin.site.register(Expense,ToShowAttributesInExpenses)
admin.site.register(Category)

