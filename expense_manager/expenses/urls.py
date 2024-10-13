from django.urls import path,include
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',views.index,name='expenses'),
    path('add-expenses',views.add_expense,name='add-expenses'),
    path('edit-expenses/<int:id>',views.edit_expenses , name='edit-expenses'),
    path('delete-expenses/<int:id>',views.delete_expenses, name='delete-expenses'),
    path("search-expenses/", csrf_exempt(views.search_expenses), name="search-expenses")
]