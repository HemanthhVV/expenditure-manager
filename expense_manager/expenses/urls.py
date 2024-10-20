from django.urls import path,include
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',views.index,name='expenses'),
    path('add-expenses',views.add_expense,name='add-expenses'),
    path('edit-expenses/<int:id>',views.edit_expenses , name='edit-expenses'),
    path('delete-expenses/<int:id>',views.delete_expenses, name='delete-expenses'),
    path("search-expenses/", csrf_exempt(views.search_expenses), name="search-expenses"),
    path("expense-summary-category", csrf_exempt(views.expense_summary_category), name="expense-summary-category"),
    path("stats-expenses/",views.stats_expenses, name="stats-expenses"),
    path("export-csv",views.export_csv,name='export-csv-expense'),
    path("export-xlsx",views.export_excel, name="export-xlsx-expense"),
    path("export-pdf", views.export_pdf, name="export-pdf-expense")
]