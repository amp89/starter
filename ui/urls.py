from django.urls import path
from ui import views

app_name = 'ui'

urlpatterns = [
    path("login", views.LoginView.as_view(), name='login'),
    path("logout", views.LogoutView.as_view(), name='logout'),
    path("password", views.PasswordView.as_view(), name='password'),
    path('codes/', views.ActivationCodesView.as_view(), name="codes"),
    
    path('clear_codes/', views.ClearOldActivationCodesView.as_view(), name="clear_codes"),

    path('sign_up/<str:code>/', views.SignupView.as_view(), name="sign_up"),
    
    path('', views.HomeView.as_view(), name='home'),

]

