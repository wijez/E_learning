from django.urls import path
from E_learning.app import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('verify-code/', views.VerifyCodeView.as_view(), name='verify-code'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('me/', views.GetMeView.as_view(), name='get-me'),
    path('reset-password', views.ResetPasswordView.as_view(), name='reset-password'),
    path('reset-password-verify', views.ResetPasswordVerifyView.as_view(), name='reset-password-verify')
]
