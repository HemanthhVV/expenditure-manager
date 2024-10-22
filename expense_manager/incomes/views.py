from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Income,Source
from django.core.paginator import Paginator
from django.http import JsonResponse,HttpResponse
import json,xlwt,csv
from userpreferences.models import UserPreference
import datetime
from collections import defaultdict
from django.db.models import Count
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Create your views here.
def export_pdf(request):
    # Create the HttpResponse object with the appropriate PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Income_'+str(datetime.date.today())+'.pdf'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 16)
    image_path = '../expense_manager/expense_manager/static/img/expense.png'  # Replace with your image file path
    p.drawImage(image_path, 100, height - 80, width=80, height=60)
    p.drawString(100, height - 100, "Income Report")  # Header title
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 120, f"Generated on: {datetime.date.today()}")  # Subheader

    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, height - 150, "Amount")
    p.drawString(200, height - 150, "Date")
    p.drawString(300, height - 150, "Description")
    p.drawString(400, height - 150, "Source")

    y_position = height - 180  # Start position for the table rows
    objs = Income.objects.filter(owner=request.user)
    for obj in objs:
        p.setFont("Helvetica", 12)
        p.drawString(100, y_position, str(obj.amount))
        p.drawString(200, y_position, str(obj.date))
        p.drawString(300, y_position, obj.description)
        p.drawString(400, y_position, obj.source)
        y_position -= 20  # Move down for the next row

    # Custom footer
    p.setFont("Helvetica-Oblique", 8)
    p.drawString(100, 20, "Income Report downloaded from Expenditure manager")

    p.showPage()
    p.save()

    return response

def export_excel(request):
    response = HttpResponse(content_type='type/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Income_'+str(datetime.date.today())+'.xlsx'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Expenses")
    row_num = 0
    columns = ['Amount','Date','Description','Source']

    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num])

    objs = Income.objects.values_list('amount','date','description','source')
    for obj in objs:
        row_num+=1
        for col_num in range(len(obj)):
            ws.write(row_num,col_num,obj[col_num])
    wb.save(response)
    return response

def export_csv(request):
    response = HttpResponse(content_type='type/csv')
    response['Content-Disposition'] = 'attachment; filename=Income_'+str(datetime.date.today())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['Amount','Date','Description','Source'])
    objs = Income.objects.filter(owner=request.user)
    for obj in objs:
        writer.writerow([obj.amount,obj.date,obj.description,obj.source])
    return response

def stats_incomes(request):
    return render(request,"expense/stats_incomes.html")

def income_summary_category(request):
    if request.method == 'GET':
        today_date = datetime.date.today()
        filtered_date = today_date - datetime.timedelta(30*6)
        all_data = Income.objects.filter(owner=request.user).values_list("date","amount").order_by('date')
        # category_wise = dict(Counter(Income.objects.values_list('source')))
        category_wise_data = Income.objects.filter(owner=request.user).values('source')\
                            .annotate(source_count=Count('source'))\
                                .values_list('source','source_count')
        category_data = {k:v for k,v in category_wise_data}
        date_wise_data = {k.strftime("%Y-%m-%d"):v for k,v in all_data}
        expenses = Income.objects.filter(
            owner=request.user,
            date__gte=filtered_date,date__lte=today_date
            )
        expense_wise = defaultdict(int)
        for expense in expenses:
            expense_wise[expense.source] += expense.amount
        return JsonResponse({'expense_wise':expense_wise,'date_wise':date_wise_data,'category_wise':category_data},safe=False)


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
        import pdb
        pdb.set_trace()
        return JsonResponse(list(search_data),safe=False)

def new_registerer(request):
    return render(request,'income/empty.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    income = Income.objects.filter(owner=request.user)
    if not income:
        return redirect('new-user-income')
    paginator = Paginator(income,3)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator,page_number)
    try:
        user_currency = UserPreference.objects.get(user = request.user)
    except:
        messages.info(request,"Please the preferred currency in order to add expenditure")
        return redirect('preferences')
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