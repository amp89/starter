
from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('activation_code_api/', include('activation_code_api.urls', namespace='activation_code_api')),
    path('', include('ui.urls', namespace='ui')),
]
