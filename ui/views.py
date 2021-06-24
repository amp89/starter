from django.shortcuts import render
from django.shortcuts import redirect
from activation_code_api.models import ActivationCode
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.core.management import call_command
from logger import logger
from django.contrib import messages
from activation_code_api.modules.helpers import Helpers
from activation_code_api.exceptions import InvalidCodeException
from activation_code_api.exceptions import ExpiredCodeException
from activation_code_api.exceptions import PasswordDoesNotMatchException
from activation_code_api.exceptions import UserExistsException
from view_classes import SuperUserView

class HomeView(LoginRequiredMixin, View):
    '''
    Home Page View
    '''
    def get(self, request, *args, **kwargs):
        return render(request, 'ui/home.html')

class LoginView(View):
    '''
    Login page view
    '''
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
    '''
    Signup View (requires access code in URL)
    '''
    def get(self, request, code):
        if request.user.is_authenticated:
            messages.error(request, "You are already logged in.")
            return redirect("ui:home")            
        try:
            valid = Helpers.check_activation_code(code=code)
            assert valid == True
            return render(request, 'ui/signup.html', {'code':code})
        except InvalidCodeException:
            messages.error(request, 'Activation Code Incorrect')
            logger.info(f"Invalid code attempt: {code}")
            return render(request, 'ui/login.html')
        except ExpiredCodeException:
            messages.error(request, 'Activation Code Has Expired')
            logger.info(f"Expired code attempt: {code}")
            return render(request, 'ui/login.html')

    def post(self, request, code):
        code = request.POST['code']
        username = request.POST['username'].lower()
        pwd = request.POST['p1']
        pwd_conf = request.POST['p2']

        try:
            new_user = Helpers.create_new_user_from_activation_code(
                code=code,
                username=username,
                pwd=pwd,
                pwd_conf=pwd_conf,
            )
            login(request, new_user)
            messages.success(request, f"Thank you for signing up, {new_user.username}!")
            return redirect("ui:home")
            return render(request, 'ui/login.html')
        except InvalidCodeException:
            messages.error(request, 'Activation Code Incorrect')
            logger.error(f"Invalid code attempt on POST: {code}")
            return render(request, 'ui/login.html')
        except ExpiredCodeException:
            messages.error(request, 'Activation Code Expired')
            return render(request, 'ui/login.html')
        except UserExistsException:
            messages.error(request, "This user already exists! Either login if you already have an account, or try again with a different username.")
            logger.info(f"User duplicate attempted: {str(username)}")
            return render(request, 'ui/signup.html', {'code':code,  'username':username})
        except PasswordDoesNotMatchException:
            messages.error(request, "Password and password confirmation must match! Please try again")
            return render(request, 'ui/signup.html', {'code':code,  'username':username})
        except Exception as e:
            logger.critical(str(e))
            messages.error(request, "Unable to create account.")
            return render(request, 'ui/signup.html', {'code':code,  'username':username})


class PasswordView(LoginRequiredMixin, View):
    '''
    View to change password
    '''
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
            Helpers.validate_password(pwd=pwd)
        except Exception as e:
            messages.error(request, f"There was a problem with your password: {str(e)}. Please try again.")
            return render(request, 'ui/password.html')

        try:
            Helpers.compare_passwords(pwd, pwd_conf)
        except PasswordDoesNotMatchException:
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
    '''
    Logout View
    '''
    def get(self, request):
        logout(request)
        return redirect("ui:login")

class ActivationCodesView(SuperUserView):
    '''
    Activation Code view (create/view codes). Requires Superuser
    '''
    def get(self, request):        
        codes = ActivationCode.objects.all().order_by("-expiration_timestamp")
        return render(request, "ui/codes.html", {"codes":codes})
        
    def post(self, request):
        hours = int(request.POST['hours'])
        if hours < 1 or hours > 8760:
            messages.error(request, "Hours must be between 1 and 8760")
            return redirect("ui:codes")
        is_once = True if request.POST.get('once') else False
        call_command('make_code', hours=hours, one_time=is_once)
        messages.success(request,"Code Created!")
        return redirect("ui:codes")

class ClearOldActivationCodesView(SuperUserView):
    '''
    Delete Activation Codes View. Requires Supersuser.
    '''
    def post(self, request):
        call_command("clear_old_codes", confirm=True)
        return redirect("ui:codes")
