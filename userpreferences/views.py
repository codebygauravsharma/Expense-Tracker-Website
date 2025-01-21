from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import UserPrferences
from django.contrib import messages
# Create your views here.
def index(request):
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR,'currencies.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for key,value in data.items():
            currency_data.append({"name":key , "value":value})

    exists = user_perfrences = UserPrferences.objects.filter(user = request.user).exists()
    user_perfrences = None

    if exists:
        user_perfrences = UserPrferences.objects.get(user = request.user)

    if request.method == 'GET':

        return render(request, 'preferences/index.html', {'currencies':currency_data, 'user_perfrences':user_perfrences})
    else:
        currency = request.POST['currency']
        if exists:
            user_perfrences.currency = currency
            user_perfrences.save()
        else:
            UserPrferences.objects.create(user = request.user, currency = currency)
        messages.success(request, f'Changes Saved {currency}')
        return render(request, 'preferences/index.html', {'currencies':currency_data, 'user_perfrences':user_perfrences})