from asyncio.log import logger
from django.shortcuts import render,redirect
import json,os
from django.conf import settings
from .models import UserPreference
from django.contrib import messages
# Create your views here.

def index(request):
    exists = UserPreference.objects.filter(user=request.user).exists()
    userpreference = None
    if exists:
        userpreference = UserPreference.objects.get(user=request.user)
    currency_data = []
    file = os.path.join(settings.BASE_DIR,"currencies.json")
    with open(file=file,mode="r") as currencies:
        currencies = json.load(currencies)
    for curr,coun in currencies.items():
        currency_data.append({'name':curr,'country':coun})

    if request.method == "GET":
        return render(request,'preferences/index.html',{'currencies':currency_data,'userpreference':userpreference})

    else:
        currency_selected = request.POST['currency']
        if exists:
            userpreference.currency = currency_selected
            userpreference.save()
        else:
            UserPreference.objects.update(user=request.user,currency=currency_selected)
        messages.success(request,"Preferences saved Successfully.")
        # print("=================> ",str(currency_selected))
        # print("=================> ",currency_selected['curr'])
        # return render(request,'preferences/index.html',{'currencies':currency_data,'userpreference':userpreference})
        return redirect('expenses')
