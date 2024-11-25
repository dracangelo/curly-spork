from django.urls import path
from .views import FinancialSettingsView, IncomeDataView, ForecastDataView

urlpatterns = [
    path('settings/', FinancialSettingsView.as_view(), name='settings'),
    path('income/', IncomeDataView.as_view(), name='income'),
    path('forecast/', ForecastDataView.as_view(), name='forecast'),
]
