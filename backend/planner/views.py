from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import FinancialSettings, IncomeData, ForecastData
from .serializers import FinancialSettingsSerializer, IncomeDataSerializer, ForecastDataSerializer
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def income(request):
    """
    Handles income and spending data to calculate the remaining balance.
    """
    if request.method == 'POST':
        try:
            # Parse incoming JSON data
            data = json.loads(request.body)
            income = data.get('income')
            spending = data.get('spending')

            if income is None or spending is None:
                return JsonResponse({'error': 'Income and spending are required fields.'}, status=400)

            # Calculate remaining balance
            remaining = income - spending

            # Optionally, save this to the database (commented out here)
            # IncomeData.objects.create(user=request.user, income=income, spending=spending, remaining=remaining)

            return JsonResponse({'income': income, 'spending': spending, 'remaining': remaining}, status=200)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)


@csrf_exempt
def signup(request):
    """
    Handles user registration.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return JsonResponse({'error': 'Email and password are required.'}, status=400)

            if User.objects.filter(username=email).exists():
                return JsonResponse({'error': 'User already exists.'}, status=400)

            # Create a new user
            user = User.objects.create_user(username=email, password=password)
            return JsonResponse({
                'message': 'User created successfully.',
                'user': {'email': user.username}
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)


class FinancialSettingsView(APIView):
    """
    Manages financial settings for the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            settings = FinancialSettings.objects.get(user=request.user)
            serializer = FinancialSettingsSerializer(settings)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except FinancialSettings.DoesNotExist:
            return Response({'error': 'Settings not found.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        settings, _ = FinancialSettings.objects.get_or_create(user=request.user)
        serializer = FinancialSettingsSerializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IncomeDataView(APIView):
    """
    Handles income data for the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        income = IncomeData.objects.filter(user=request.user)
        serializer = IncomeDataSerializer(income, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = IncomeDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForecastDataView(APIView):
    """
    Handles forecast data for the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        forecast = ForecastData.objects.filter(user=request.user)
        serializer = ForecastDataSerializer(forecast, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ForecastDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
