from django.shortcuts import render
from django.shortcuts import reverse
from django.shortcuts import redirect
from api.models import ActivationCode
from django.http import HttpResponseBadRequest
from django.http import HttpResponseForbidden
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
import django.contrib.auth.password_validation as validators
from django.contrib.auth import authenticate, login, logout
from django.core.management import call_command

from django.contrib import messages
class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'ui/index.html')

class ExampleLoginRequiredView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("hi")

class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("ui:home")
        return render(request, 'ui/login.html')

    def post(self, request):        
        username = request.POST['u'].lower()
        pwd = request.POST['p']
        
        user = authenticate(request, username=username, password=pwd)

        if user is not None:
            login(request, user)
            return redirect("ui:home")
        else:
            messages.error(request, 'Login Incorrect')
            return render(request, 'ui/login.html')

class SignupView(View):
    def get(self, request, code):
        if request.user.is_authenticated:
            return redirect("ui:home")
        
        try:
            activation_code = ActivationCode.objects.get(code=code)
        except ActivationCode.DoesNotExist:
            messages.error(request, 'Activation Code Incorrect')
            print(code)
            return render(request, 'ui/login.html')

        if activation_code.check_validity() == False:
            messages.error(request, 'Activation Code Has Expired')
            return render(request, 'ui/login.html')
        else:                
            return render(request, 'ui/signup.html', {'code':code})
        


    def post(self, request, code):
        code = request.POST['code']
        username = request.POST['username'].lower()
        pwd = request.POST['p1']
        pwd_conf = request.POST['p2']

        # TODO abstract some of this stuff pls.. move things to other scripts
        try:
            activation_code = ActivationCode.objects.get(code=code)
        except:
            messages.error(request, 'Activation Code Incorrect')
            return render(request, 'ui/login.html')

        if activation_code.check_validity() == False:
            messages.error(request, 'Activation Code Incorrect')
            return render(request, 'ui/login.html')
        

        try:
            validators.validate_password(password=pwd, user=User)
        except Exception as e:
            messages.error(request, f"Problem with your password: {str(e)}") # TODO catch more specific error
            print("pwd issue")
            return render(request, 'ui/signup.html', {'code':code, 'username':username})
        
        
        if not pwd or not pwd_conf or pwd != pwd_conf:
            messages.error(request, "Passwords must match! Please try again")
            return render(request, 'ui/signup.html', {'code':code,  'username':username})

        try:
            if User.objects.filter(username__iexact=username).exists():            
                messages.error(request, "This user already exists! Either login, or try again with a different username.")
                return render(request, 'ui/signup.html', {'code':code,  'username':username})
        except User.DoesNotExist:
            pass

        u = User(username=username)
        u.set_password(pwd)
        u.save()        

        new_user = authenticate(request, username=username, password=pwd)

        if new_user is not None:
            if activation_code.one_time_use:
                activation_code.force_invalidate()
            login(request, new_user)
            messages.success(request, "Thank you for signing up!")
            return redirect("ui:home")
        else:
            return redirect("ui:login")

class PasswordView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'ui/password.html')

    def post(self, request):
        old_pwd = request.POST['p']
        pwd = request.POST['p1']
        pwd_conf = request.POST['p2']

        this_user = authenticate(request, username=request.user.username, password=old_pwd)
        if not this_user:
            messages.error(request, "Your old password was incorrect")
            return render(request, 'ui/password.html')

        try:
            validators.validate_password(password=pwd, user=User)
        except Exception as e:
            messages.error(request, f"There was a problem with your password: {str(e)}. Please try again.")
            return render(request, 'ui/password.html')

        if not pwd or not pwd_conf or pwd != pwd_conf:
            messages.error(request, 'Passwords must match! Please Try again')
            return render(request, 'ui/password.html')

        this_user.set_password(pwd)
        this_user.save()
        
        logout(request)

        new_p_user = authenticate(request, username=this_user.username.lower(), password=pwd)

        if new_p_user is not None:
            login(request, new_p_user)
            messages.success(request, 'Your password has been changed!')
            return redirect("ui:home")
        else:
            messages.error(request, 'Unable to change password. Please login again.')
            return redirect("ui:login")

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect("ui:login")

class ActivationCodesView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_superuser:
            # codes = ActivationCode.objects.all().order_by("-expiration_timestamp")
            codes = ActivationCode.objects.all().order_by("-pk")
            return render(request, "ui/codes.html", {"codes":codes})
        else:
            return HttpResponseForbidden()

    def post(self, request):
        if not request.user.is_superuser:
            return HttpResponseForbidden()

        hours = int(request.POST['hours'])
        if hours < 1 or hours > 8760:
            messages.error(request, "Hours must be between 1 and 8760")
            return redirect("ui:codes")
        is_once = True if request.POST.get('once') else False
        call_command('make_code', hours=hours, one_time=is_once)
        messages.success(request,"Code Created!")
        return redirect("ui:codes")

class ClearOldActivationCodesView(LoginRequiredMixin, View):
    def post(self, request):
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        call_command("clear_old_codes", confirm=True)
        return redirect("ui:codes")
