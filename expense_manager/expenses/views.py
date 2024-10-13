from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Category,Expense
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from userpreferences.models import UserPreference

# Create your views here.

def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get("searchField")
        expenses = (
                    Expense.objects.filter(amount__istartswith=search_str,owner = request.user) |
                    Expense.objects.filter(date__istartswith=search_str,owner = request.user) |
                    Expense.objects.filter(description__icontains=search_str,owner = request.user) |
                    Expense.objects.filter(category__icontains=search_str,owner = request.user)
                    )

        search_data = expenses.values()
        return JsonResponse(list(search_data),safe=False)





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    expense = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expense,3)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator,page_number)
    user_currency = UserPreference.objects.get(user = request.user)
    context = {
        "expenses" : expense,
        "page_obj" : page_obj,
        "user_currency" : user_currency.currency
    }
    return render(request,'expense/index.html',context=context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_expense(request):
    category = Category.objects.all()
    expense = Expense.objects.filter(owner=request.user)
    context = {
        'categories':category,
        'value':request.POST,
        'expenses':expense
    }
    # print(request.method)
    if request.method == 'GET':
        return render(request,'expense/add_expense.html',context=context)
    else:
        amount = request.POST['amount_field']
        date = request.POST['date_field']
        description = request.POST['description_field']
        category = request.POST['category_field']

        if not amount:
            messages.error(request=request,message="Fill the amount")
            return render(request,'expense/add_expense.html',context=context)
        if not date:
            messages.error(request=request,message="Fill the date")
            return render(request,'expense/add_expense.html',context=context)
        if not description:
            messages.error(request=request,message="Description should least contains a word")
            return render(request,'expense/add_expense.html',context=context)

        Expense.objects.create(amount=amount,date=date,description=description,owner=request.user,category=category)
        messages.success(request,"Expenses addded successfully")
        return redirect('expenses')
        # return render(request,'expense/index.html',context=context)

def edit_expenses(request,id):
    expense = Expense.objects.get(pk = id)
    category = Category.objects.all()
    context = {
        'expenses':expense,
        'value':expense,
        'categories':category,
    }
    if request.method == 'GET':
        return render(request=request,template_name='expense/edit_expense.html',context=context)
    else:
        amount = request.POST['amount_field']
        date = request.POST['date_field']
        description = request.POST['description_field']
        category = request.POST['category_field']

        if not amount:
            messages.error(request=request,message="Fill the amount")
            return render(request,'expense/edit_expense.html',context=context)
        if not date:
            messages.error(request=request,message="Fill the date")
            return render(request,'expense/edit_expense.html',context=context)
        if not description:
            messages.error(request=request,message="Description should least contains a word")
            return render(request,'expense/edit_expense.html',context=context)

        expense.amount=amount
        expense.date=date
        expense.description=description
        expense.owner=request.user
        expense.category=category

        expense.save()
        messages.success(request,"Expenses Updated successfully")
        return redirect('expenses')


def delete_expenses(request,id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    return redirect('expenses')