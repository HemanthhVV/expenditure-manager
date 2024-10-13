from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Income,Source
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from userpreferences.models import UserPreference

# Create your views here.

def search_incomes(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get("searchField")
        expenses = (
                    Income.objects.filter(amount__istartswith=search_str,owner = request.user) |
                    Income.objects.filter(date__istartswith=search_str,owner = request.user) |
                    Income.objects.filter(description__icontains=search_str,owner = request.user) |
                    Income.objects.filter(source__icontains=search_str,owner = request.user)
                    )

        search_data = expenses.values()
        return JsonResponse(list(search_data),safe=False)





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    income = Income.objects.filter(owner=request.user)
    paginator = Paginator(income,3)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator,page_number)
    user_currency = UserPreference.objects.get(user = request.user)
    context = {
        "incomes" : income,
        "page_obj" : page_obj,
        "user_currency" : user_currency.currency
    }
    return render(request,'income/index.html',context=context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_income(request):
    source = Source.objects.all()
    income = Income.objects.filter(owner=request.user)
    context = {
        'sources':source,
        'value':request.POST,
        'incomes':income
    }
    # print(request.method)
    if request.method == 'GET':
        return render(request,'income/add_income.html',context=context)
    else:
        amount = request.POST['amount_field']
        date = request.POST['date_field']
        description = request.POST['description_field']
        source = request.POST['source_field']

        if not amount:
            messages.error(request=request,message="Fill the amount")
            return render(request,'income/add_income.html',context=context)
        if not date:
            messages.error(request=request,message="Fill the date")
            return render(request,'income/add_income.html',context=context)
        if not description:
            messages.error(request=request,message="Description should least contains a word")
            return render(request,'income/add_income.html',context=context)

        Income.objects.create(amount=amount,date=date,description=description,owner=request.user,source=source)
        messages.success(request,"Income added successfully")
        return redirect('incomes')
        # return render(request,'income/index.html',context=context)

def edit_incomes(request,id):
    income = Income.objects.get(pk = id)
    source = Source.objects.all()
    context = {
        'incomes':income,
        'value':income,
        'categories':source,
    }
    if request.method == 'GET':
        return render(request=request,template_name='income/edit_income.html',context=context)
    else:
        amount = request.POST['amount_field']
        date = request.POST['date_field']
        description = request.POST['description_field']
        source = request.POST['source_field']

        if not amount:
            messages.error(request=request,message="Fill the amount")
            return render(request,'income/edit_income.html',context=context)
        if not date:
            messages.error(request=request,message="Fill the date")
            return render(request,'income/edit_income.html',context=context)
        if not description:
            messages.error(request=request,message="Description should least contains a word")
            return render(request,'income/edit_income.html',context=context)

        income.amount=amount
        income.date=date
        income.description=description
        income.owner=request.user
        income.source=source

        income.save()
        messages.success(request,"Income Updated successfully")
        return redirect('incomes')


def delete_incomes(request,id):
    income = Income.objects.get(pk=id)
    income.delete()
    return redirect('incomes')