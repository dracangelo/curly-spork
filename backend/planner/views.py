from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import FinancialSettings, IncomeData, ForecastData
from .serializers import FinancialSettingsSerializer, IncomeDataSerializer, ForecastDataSerializer
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def signup(request):
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
            return JsonResponse({'message': 'User created successfully.', 'user': {'email': user.username}}, status=201)
        except Exception as e:
            return JsonResponse({'error': 'An error occurred.'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

class FinancialSettingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        settings = FinancialSettings.objects.get(user=request.user)
        serializer = FinancialSettingsSerializer(settings)
        return Response(serializer.data)

    def post(self, request):
        settings, created = FinancialSettings.objects.get_or_create(user=request.user)
        serializer = FinancialSettingsSerializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class IncomeDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        income = IncomeData.objects.filter(user=request.user)
        serializer = IncomeDataSerializer(income, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = IncomeDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class ForecastDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        forecast = ForecastData.objects.filter(user=request.user)
        serializer = ForecastDataSerializer(forecast, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ForecastDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
