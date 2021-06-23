
from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path("health_check", views.HealthCheckView.as_view(), name='health_check'),
    path("auth_health_check", views.AuthHealthCheckView.as_view(), name='auth_health_check'),
]
