from django.urls import path
from .import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('',views.index, name='expenses'),
    path('add_expenses',views.add_expenses, name='add_expenses'),
    path('edit_expense/<int:id>',views.edit_expense, name='edit_expense'),
    path('delete_expense/<int:id>',views.delete_expense, name='delete_expense'),
    path('search-expenses',csrf_exempt(views.search_expenses), name='search-expenses'),
    path('download_expenses_report',views.download_report, name='download_expenses_report'),
    path('export_csv',views.export_csv, name='export-csv'),
    path('export_excel',views.export_excel, name='export-excel'),
    path('export_pdf',views.export_pdf, name='export-pdf'),

]
