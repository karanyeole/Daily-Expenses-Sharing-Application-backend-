# expenses_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('create-user/', views.create_user, name='create_user'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('user-expenses/<int:user_id>/', views.retrieve_user_expenses, name='retrieve_user_expenses'),
    path('overall-expenses/', views.retrieve_overall_expenses, name='retrieve_overall_expenses'),
    path('download-balance-sheet/', views.download_balance_sheet, name='download_balance_sheet'),
]
