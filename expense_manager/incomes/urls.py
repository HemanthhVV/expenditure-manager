from django.urls import path,include
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',views.index,name='incomes'),
    path('add-incomes',views.add_income,name='add-incomes'),
    path('edit-incomes/<int:id>',views.edit_incomes, name='edit-incomes'),
    path('delete-incomes/<int:id>',views.delete_incomes, name='delete-incomes'),
    path("search-incomes/", csrf_exempt(views.search_incomes), name="search-incomes"),
    path("income-summary-category", csrf_exempt(views.income_summary_category), name="income-summary-category"),
    path("stats-incomes/",views.stats_incomes, name="stats-incomes"),
    path("export-csv",views.export_csv,name='export-csv'),
    path("export-xlsx",views.export_excel, name="export-xlsx"),
    path("export-pdf", views.export_pdf, name="export-pdf"),
    path("new-user",views.new_registerer,name="new-user-income"),
]