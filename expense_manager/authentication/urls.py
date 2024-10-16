from django.urls import path,include
from . import views
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('',views.RegistrationView.as_view(),name="register"),
    path('validateUser',csrf_exempt(views.UserValidation.as_view()),name="uservalidation"),
    path('validateEmail',csrf_exempt(views.EmailValidation.as_view()), name="emailvalidation"),
    path('verificationEmail/<uuid>/<token>',views.VerificationView.as_view(),name='verification'),
    path('login',csrf_exempt(views.LoginView.as_view()),name="login"),
    path('logout',csrf_exempt(views.LogoutView.as_view()),name="logout"),
    path("reset-password",csrf_exempt(views.ResetPasswordView.as_view()) , name="reset-password"),
    path("set-new-password/<uuid>/<token>", csrf_exempt(views.SetNewPassword.as_view()), name="set-new-password")
]
