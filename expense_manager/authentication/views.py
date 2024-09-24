from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
# from email_validator import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage,send_mail
from django.core.validators import validate_email
from django.conf import settings

# from django.core.mail.backends.smtp import EmailBackend
# Create your views here.


class EmailValidation(View):
    def post(self,request):
        print(request)
        data = json.loads(request.body)
        email = data['email']
        try :
            validation = validate_email(email)
        except :
            return JsonResponse({'email_error':'email is not valid'},status=405)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'email is already taken'},status = 402)
        return JsonResponse({'email_valid':True})


class UserValidation(View):
    def post(self,request):
        print(request)
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should only contains the alphanumeric characters'},status=405)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'username is already taken'},status = 402)
        return JsonResponse({'username_valid':True})


class RegistrationView(View):
    def get(self,request):
        return render(request=request,template_name="authentication/register.html")
    def post(self,request):
        body = request.POST
        context = {
            "fieldValues":body
        }
        username = body["username"]
        email = body["email"]
        password = body["password"]


        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 8:
                    messages.error(request=request,message="Password should contains minimum length 8")
                    return render(request=request,template_name="authentication/register.html",context=context)
                user = User.objects.create(username = username,email=email)
                user.set_password(password)
                user.is_active = False
                print(settings.EMAIL_HOST_USER)
                verification_mail_sent = send_mail(
                    subject="Registered Sucessfully!",
                    message="Thanks for registering in this app, None of your data has been cached.",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[
                        email
                    ],
                    fail_silently=False
                )
                user.save()
                messages.success(request=request,message="User Registered Successfully")
                return render(request=request,template_name="authentication/register.html")
            else:
                messages.warning(request=request,message="Email address already exists")
                return render(request=request,template_name="authentication/register.html",context=context)
        else:
            messages.warning(request=request,message="Username already exists")
            return render(request=request,template_name="authentication/register.html",context=context)
