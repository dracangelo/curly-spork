from django.db import models
from django.contrib.auth.models import User

class FinancialSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    income_target = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    savings_goal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    spending_limit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Financial Settings"


class IncomeData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} on {self.date}"


class ForecastData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    income = models.DecimalField(max_digits=10, decimal_places=2)
    spending = models.DecimalField(max_digits=10, decimal_places=2)
    forecasted_savings = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Forecast for {self.user.username} on {self.date_created}"
