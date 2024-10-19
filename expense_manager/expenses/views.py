from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Category,Expense
from django.core.paginator import Paginator
from django.http import JsonResponse,HttpResponse
import json
from collections import defaultdict,Counter
from userpreferences.models import UserPreference
import datetime,csv,xlwt
from django.db.models import Count

# Create your views here.
def export_excel(request):
    response = HttpResponse(content_type='type/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Expenses_'+str(datetime.date.today())+'.xlsx'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Expenses")
    row_num = 0
    columns = ['Amount','Date','Description','Category']

    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num])

    objs = Expense.objects.values_list('amount','date','description','category')
    for obj in objs:
        row_num+=1
        for col_num in range(len(obj)):
            ws.write(row_num,col_num,obj[col_num])
    wb.save(response)
    return response

def export_csv(request):
    response = HttpResponse(content_type='type/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses_'+str(datetime.date.today())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['Amount','Date','Description','Category'])
    objs = Expense.objects.filter(owner=request.user)
    for obj in objs:
        writer.writerow([obj.amount,obj.date,obj.description,obj.category])
    return response

def stats_expenses(request):
    return render(request,"expense/stats_expenses.html")

def expense_summary_category(request):
    if request.method == 'GET':
        today_date = datetime.date.today()
        filtered_date = today_date - datetime.timedelta(30*6)
        all_data = Expense.objects.values_list("date","amount").order_by('date')
        # category_wise = dict(Counter(Expense.objects.values_list('category')))
        category_wise_data = Expense.objects.values('category')\
                            .annotate(category_count=Count('category'))\
                                .values_list('category','category_count')
        category_data = {k:v for k,v in category_wise_data}
        date_wise_data = {k.strftime("%Y-%m-%d"):v for k,v in all_data}
        expenses = Expense.objects.filter(
            owner=request.user,
            date__gte=filtered_date,date__lte=today_date
            )
        expense_wise = defaultdict(int)
        for expense in expenses:
            expense_wise[expense.category] += expense.amount
        return JsonResponse({'expense_wise':expense_wise,'date_wise':date_wise_data,'category_wise':category_data},safe=False)


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