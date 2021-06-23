from django.shortcuts import render

from rest_framework.views import APIView
from view_classes import APIAuthView

class HealthCheckView(APIView):
    def get(self, request):
        return Response({},status=status.HTTP_200_OK)

class AuthHealthCheckView(APIAuthView):
    def get(self, request):
        return Response({},status=status.HTTP_200_OK)

