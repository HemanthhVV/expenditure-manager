from django.contrib import admin
from .models import Income,Source
# Register your models here.

class ToShowAttributesIncome(admin.ModelAdmin):
    list_display =("amount",
                    "date",
                    "description",
                    "owner",
                    "source",
                    )
    search_fields =(
                    "date",
                    "description",
                    "source",
                    )

admin.site.register(Income,ToShowAttributesIncome)
admin.site.register(Source)