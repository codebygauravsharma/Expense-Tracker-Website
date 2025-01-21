from django.shortcuts import render, redirect
from .models import Category, Expense
from userpreferences.models import UserPrferences
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse
import csv
import datetime
import xlwt
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.db.models import Sum 
# Create your views here.


@login_required(login_url="/authentication/login")
def index(request):
    get_expense = Expense.objects.filter(owner = request.user)

    show_all = request.GET.get("page") == 'all'
    if show_all:
        page_obj = get_expense
    else:
        paginator = Paginator(get_expense, 5)
        page_number = request.GET.get("page")
        page_obj = Paginator.get_page(paginator, page_number)
    
    user_preferences, created = UserPrferences.objects.get_or_create(
        user=request.user,
        defaults={'currency': 'USD'}
    )
    currency = user_preferences.currency

    # currency = UserPrferences.objects.get(user = request.user).currency
          
    context = {
            "get_expense":get_expense,
            "page_obj":page_obj,
            "show_all":show_all,
            "currency":currency
    }
    return render(request, 'expensesapp/index.html', context)


def add_expenses(request):
    categories = Category.objects.all()
    context={
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'expensesapp/add_expense.html', context )

    if request.method == 'POST':
        description = request.POST['description']
        amount = request.POST['amount']
        category = request.POST['category']
        expense_date = request.POST['expense_date']

        if not amount: 
            messages.error(request, "Amount is Required")

        if not description: 
            messages.error(request, "Description is Required")

        if not category: 
            messages.error(request, "Category is Required")

        if not expense_date: 
            messages.error(request, "Date is Required")

        if messages.get_messages(request):
            return render(request, 'expensesapp/add_expense.html', context )

        Expense.objects.create(owner=request.user, amount=amount,description=description,date=expense_date,category=category)

        messages.success(request, "Expense added successfully.")
        return redirect('expenses')

def edit_expense(request, id):
    get_expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        "get_expense":get_expense,
        "values":get_expense,
        "categories":categories,
    }
    if request.method == 'GET':
        return render(request, 'expensesapp/edit_expense.html',context)
    
    if request.method == 'POST':
        description = request.POST['description']
        amount = request.POST['amount']
        category = request.POST['category']
        expense_date = request.POST['expense_date']

        if not amount: 
            messages.error(request, "Amount is Required")

        if not description: 
            messages.error(request, "Description is Required")

        if not category: 
            messages.error(request, "Category is Required")

        if not expense_date: 
            messages.error(request, "Date is Required")

        if messages.get_messages(request):
            return render(request, 'expensesapp/edit_expense.html', context )

        get_expense.owner=request.user
        get_expense.amount=amount
        get_expense.description=description
        get_expense.date=expense_date
        get_expense.category=category

        get_expense.save()

        messages.success(request, "Expense Updated successfully.")
        return redirect('expenses')
    
def delete_expense(request, id):
    get_expense = Expense.objects.get(pk=id)
    get_expense.delete()
    messages.success(request, "Expense Deleted successfully.")
    return redirect('expenses')

def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        expenses = Expense.objects.filter(amount__istartswith = search_str, owner= request.user) | Expense.objects.filter(
            date__istartswith = search_str, owner= request.user) | Expense.objects.filter(
                description__icontains = search_str, owner= request.user) | Expense.objects.filter(
                category__icontains =search_str, owner=request.user)

        data = expenses.values()

        return JsonResponse(list(data), safe= False)
    

def download_report(request):
    return render(request,'expensesapp/download_report.html')

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + str(datetime.datetime.now())+'.csv'

    writer = csv.writer(response)
    writer.writerow(['Amount','Description','Category','Date'])
    expenses = Expense.objects.filter(owner = request.user)

    for expense in expenses:
        writer.writerow([expense.amount, expense.description, expense.category, expense.date])

    return response

def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + str(datetime.datetime.now())+'.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Amount','Description','Category','Date']

    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num], font_style)
    
    font_style = xlwt.XFStyle()

    rows = Expense.objects.filter(owner = request.user).values_list(
        'amount','description','category','date'
    )

    for row in rows:
        row_num +=1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)

    return response

def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=Expenses' + str(datetime.datetime.now())+'.pdf'

    response['Content-Transfer-Encoding'] = 'binary'
    expenses = Expense.objects.filter(owner = request.user)
    sum = expenses.aggregate(Sum('amount'))
    # context = {'expenses': [], 'total':0}
    html_string = render_to_string('expensesapp/pdf-output.html', {'expenses': expenses, 'total': sum['amount__sum']})

    html = HTML(string=html_string)

    pdf_file = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(pdf_file)
        output.flush()
        output.seek(0)
        response.write(output.read())
    
    return response
    