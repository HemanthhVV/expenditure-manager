from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.mail import EmailMessage,send_mail
from django.core.validators import validate_email
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from .utils import token_generator
from django import forms
from django.contrib.auth.hashers import make_password
from django.views.decorators.cache import cache_control

# from django.core.mail.backends.smtp import EmailBackend
# Create your views here.

class LogoutView(View):
    def post(self,request):
        auth.logout(request)
        messages.success(request,"Logged out Successfully")
        return redirect('login')

class LoginView(View):
    def get(self,request):
        return render(request=request,template_name='authentication/login.html')

    def post(self,request):
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        # if User.objects.filter(username=username).exists():
        #     print(username," ======-------======== ",password)
        try:
            user = User.objects.get(username=username)
        except:
            user=None
        if not user:
            messages.error(request,"You are not registered with this username,check again.")
            return render(request,'authentication/login.html')
        if user and user.check_password(password):
            if user:
                if user.is_active:
                    auth.login(request=request,user=user)
                    messages.success(request,"Login Sucessfully")
                    return redirect('expense')
                messages.error(request,"Account not activated yet, check your mail")
                return render(request,'authentication/login.html')
            messages.error(request,"Invalid Credentials, Register First")
            return render(request,'authentication/login.html')
        messages.error(request=request,message="Please fill all the fields")
        return render(request,'authentication/login.html')

class VerificationView(View):
    def get(self,request,uuid,token):
        # try:
        pk = force_str(urlsafe_base64_decode(uuid))
        print("InVErificationView============>",pk)
        userObj = User.objects.get(pk=pk)
        if userObj.is_active:
            return redirect('login')
        userObj.is_active = True
        userObj.save()
        return redirect('login')
        # except Exception:
        #     print("Exception occured at Views of Authentication ",Exception)
        # return redirect('login')

class EmailValidation(View):
    def post(self,request):
        # print("====================>",request)
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
            return JsonResponse({'username_error':'username should only contains the alphanumeric characters'},status=403)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'username is already taken'},status = 401)
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

                domain = get_current_site(request=request).domain
                uuid = urlsafe_base64_encode(force_bytes(user.pk))
                query_parameter_for_activation = reverse('verification',kwargs={'uuid':uuid,'token':token_generator.make_token(user)})
                activation_url = 'http://'+domain+query_parameter_for_activation

                user.save()

                verification_mail_sent = send_mail(
                    subject="Registered Sucessfully!",
                    message=f"Thanks for registering in this app, None of your data has been cached.\nTo Verify your mail:\n{activation_url}",
                    from_email=str(settings.EMAIL_HOST_USER),
                    recipient_list=[
                        email
                    ],
                    fail_silently=False
                )

                print("Domain printing ===== > ",domain)
                print(settings.EMAIL_HOST_USER)
                print(force_bytes(user.pk))
                print(force_str(force_bytes(user.pk)))

                messages.success(request=request,message="Register Successfully, Check your mail for activation.")
                return render(request=request,template_name="authentication/register.html")
            else:
                messages.warning(request=request,message="Email address already exists")
                return render(request=request,template_name="authentication/register.html",context=context)
        else:
            messages.warning(request=request,message="Username aleady exists")
            return render(request=request,template_name="authentication/register.html",context=context)
