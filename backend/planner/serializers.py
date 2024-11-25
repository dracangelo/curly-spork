from rest_framework import serializers
from .models import FinancialSettings, IncomeData, ForecastData

class FinancialSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialSettings
        fields = ['income_target', 'savings_goal', 'spending_limit']


class IncomeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeData
        fields = ['amount', 'date']


class ForecastDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForecastData
        fields = ['income', 'spending', 'forecasted_savings', 'date_created']
