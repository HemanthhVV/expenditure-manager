from django.urls import path,include
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('',views.RegistrationView.as_view(),name="register"),
    path('validateUser',csrf_exempt(views.UserValidation.as_view()),name="uservalidation"),
    path('validateEmail',csrf_exempt(views.EmailValidation.as_view()), name="emailvalidation")
]
