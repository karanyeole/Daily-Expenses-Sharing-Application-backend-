# expenses_app/serializers.py

from rest_framework import serializers
from .models import User, Expense

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'mobile']

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'user', 'description', 'amount', 'split_method', 'participants', 'created_at']

class ExpenseSerializer(serializers.ModelSerializer):
    amounts = serializers.ListField(child=serializers.DecimalField(max_digits=10, decimal_places=2), required=False)
    percentages = serializers.ListField(child=serializers.IntegerField(), required=False)

    class Meta:
        model = Expense
        fields = ['id', 'user', 'description', 'amount', 'split_method', 'participants', 'amounts', 'percentages', 'created_at']

    def validate(self, data):
        if data.get('split_method') == 'percentage' and sum(data.get('percentages', [])) != 100:
            raise serializers.ValidationError("Percentages must add up to 100.")
        return data