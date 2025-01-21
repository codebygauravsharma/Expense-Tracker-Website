from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import UserIncome, Source
from userpreferences.models import UserPrferences
import json
from django.http import JsonResponse

# Create your views here.

@login_required(login_url="/authentication/login")
def index(request):
    get_income = UserIncome.objects.filter(owner = request.user)
    show_all = request.GET.get("page") == 'all'

    if show_all:
        page_obj = get_income
    else:
        paginator = Paginator(get_income, 5)
        page_number = request.GET.get("page")
        page_obj = Paginator.get_page(paginator, page_number)
    
    currency = UserPrferences.objects.get(user = request.user).currency
          
    context = {
            "get_income":get_income,
            "page_obj":page_obj,
            "show_all":show_all,
            "currency":currency
    }
    return render(request, 'userincome/index.html', context)


def add_income(request):
    sources = Source.objects.all()
    context={
        'sources': sources,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'userincome/add_income.html', context )

    if request.method == 'POST':
        description = request.POST['description']
        amount = request.POST['amount']
        source = request.POST['source']
        income_date = request.POST['income_date']

        if not amount: 
            messages.error(request, "Amount is Required")

        if not description: 
            messages.error(request, "Description is Required")

        if not source: 
            messages.error(request, "Source is Required")

        if not income_date: 
            messages.error(request, "Date is Required")

        if messages.get_messages(request):
            return render(request, 'userincome/add_income.html', context )

        UserIncome.objects.create(owner=request.user, amount=amount,description=description,date=income_date,source=source)

        messages.success(request, "Income added successfully.")
        return redirect('income')
    

def edit_income(request, id):
    get_income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        "get_income":get_income,
        "values":get_income,
        'sources': sources,
    }
    if request.method == 'GET':
        return render(request, 'userincome/edit_income.html',context)
    
    if request.method == 'POST':
        description = request.POST['description']
        amount = request.POST['amount']
        source = request.POST['source']
        income_date = request.POST['income_date']

        if not amount: 
            messages.error(request, "Amount is Required")

        if not description: 
            messages.error(request, "Description is Required")

        if not source: 
            messages.error(request, "Source is Required")

        if not income_date: 
            messages.error(request, "Date is Required")

        if messages.get_messages(request):
            return render(request, 'userincome/edit_income.html', context )

        get_income.owner=request.user
        get_income.amount=amount
        get_income.description=description
        get_income.date=income_date
        get_income.category=source

        get_income.save()

        messages.success(request, "Income Updated successfully.")
        return redirect('income')
    
def delete_income(request, id):
    get_income = UserIncome.objects.get(pk=id)
    get_income.delete()
    messages.success(request, "Income Deleted successfully.")
    return redirect('income')

def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        income = UserIncome.objects.filter(amount__istartswith = search_str, owner= request.user) | UserIncome.objects.filter(
            date__istartswith = search_str, owner= request.user) | UserIncome.objects.filter(
                description__icontains = search_str, owner= request.user) | UserIncome.objects.filter(
                source__icontains =search_str, owner=request.user)

        data = income.values()

        return JsonResponse(list(data), safe= False)