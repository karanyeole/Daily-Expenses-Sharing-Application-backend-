# expenses_app/views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import User, Expense
from .serializers import UserSerializer, ExpenseSerializer
from .expenses_utils import split_equal, split_exact, split_percentage
from decimal import Decimal
import csv
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination  # Import the pagination class

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['POST'])
def create_user(request):
    """Create a new user"""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created successfully!", "user": serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Ensure user is authenticated
def add_expense(request):
    """Add a new expense"""
    try:
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            expense = serializer.save()

            # Perform the split based on method
            split_method = request.data['split_method']
            participants = request.data['participants']
            amount = Decimal(request.data['amount'])

            if split_method == 'equal':
                result = split_equal(amount, participants)
            elif split_method == 'exact':
                result = split_exact(request.data['amounts'], participants)
            elif split_method == 'percentage':
                result = split_percentage(request.data['percentages'], amount, participants)

            return Response({
                'message': "Expense added successfully!",
                'expense': serializer.data,
                'split_result': result
            }, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure user is authenticated
def retrieve_user_expenses(request, user_id):
    """Retrieve individual user expenses"""
    user = get_object_or_404(User, pk=user_id)
    if request.user.id != user.id:
        return Response({'error': 'Permission denied: You can only access your own expenses.'}, status=status.HTTP_403_FORBIDDEN)
    
    expenses = Expense.objects.filter(participants__id=user.id)
    serializer = ExpenseSerializer(expenses, many=True)
    return Response({
        'user': UserSerializer(user).data,
        'expenses': serializer.data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure user is authenticated
def retrieve_overall_expenses(request):
    """Retrieve overall expenses for all users with pagination"""
    expenses = Expense.objects.all()
    paginator = StandardResultsSetPagination()
    result_page = paginator.paginate_queryset(expenses, request)
    serializer = ExpenseSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure user is authenticated
def download_balance_sheet(request):
    """Download the balance sheet as CSV"""
    expenses = Expense.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="balance_sheet.csv"'

    writer = csv.writer(response)
    writer.writerow(['Expense ID', 'Description', 'Amount', 'Participants'])

    for expense in expenses:
        participants = ', '.join([user.name for user in expense.participants.all()])
        writer.writerow([expense.id, expense.description, expense.amount, participants])

    return response

@api_view(['GET'])
def home(request):
    """Home view for the app."""
    return HttpResponse("Welcome to the Daily Expenses Sharing Application!")

@api_view(['POST'])
def user_login(request):
    """User login"""
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(username=email, password=password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'message': 'Login successful!'}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure user is authenticated
def filter_expenses(request):
    """Filter expenses based on date, category, or amount."""
    filters = {}
    date_from = request.query_params.get('date_from')
    date_to = request.query_params.get('date_to')
    category = request.query_params.get('category')
    min_amount = request.query_params.get('min_amount')
    max_amount = request.query_params.get('max_amount')

    if date_from and date_to:
        filters['date__range'] = [date_from, date_to]
    if category:
        filters['category'] = category
    if min_amount and max_amount:
        filters['amount__range'] = [min_amount, max_amount]

    expenses = Expense.objects.filter(participants=request.user, **filters)
    serializer = ExpenseSerializer(expenses, many=True)
    return Response(serializer.data)

# Add unit tests in a separate test file, such as expenses_app/tests.py
