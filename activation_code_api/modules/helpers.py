from django.contrib.auth.models import User
from activation_code_api.exceptions import InvalidCodeException
from activation_code_api.exceptions import ExpiredCodeException
from activation_code_api.exceptions import PasswordDoesNotMatchException
from activation_code_api.exceptions import UserExistsException
from activation_code_api.models import ActivationCode
import django.contrib.auth.password_validation as validators
from logger import logger

class Helpers():

    @staticmethod
    def validate_password(pwd):
        '''
        Call validator, raise error thrown by validator if not valid
        '''
        try:
            validators.validate_password(password=pwd, user=User)
        except Exception as e:
            raise e        

    @staticmethod
    def compare_passwords(pwd, pwd_conf):
        '''
        Compare password, raise PasswordDoesNotMatchException if not valid
        Return True if valid
        '''
        assert pwd and pwd_conf, "pwd and pwd_conf are both required"

        if pwd == pwd_conf:
            return True
        else:
            raise PasswordDoesNotMatchException


    @staticmethod
    def check_activation_code(code):
        '''
        Check code - raise InvalidCodeException if not correct, 
        raise ExpiredCodeException code is not still valid
        Return True if valid
        '''
        try:
            activation_code = ActivationCode.objects.get(code=code)
        except ActivationCode.DoesNotExist as dne:
            raise InvalidCodeException
        except Exception as e:
            logger.critical(str(e))
        
        if activation_code.check_validity() == True:
            return True
        else:
            raise ExpiredCodeException

    @staticmethod
    def create_user(username, pwd):
        '''
        LOWERCASE the username (just b/c that's how I want it for convention)
        Raise UserExistsException if user already exists
        Create user
        Return new user if successful
        '''
        assert username and pwd, "username and pwd are both required"

        if User.objects.filter(username__iexact=username).exists():
            raise UserExistsException
        else:
            new_user = User(username=username)
            new_user.set_password(pwd)
            new_user.save()
            return new_user
        
    @staticmethod
    def invalidate_if_one_time_use_code(code):
        '''
        Invalidate code if it's a one time use code
        '''
        # NOTE: When used to ativate a new user, this is less effecient, but allows for better abstraction
        activation_code = ActivationCode.objects.get(code=code)
        if activation_code.one_time_use:
            activation_code.force_invalidate()

    @staticmethod
    def invalidate_code(code):
        '''
        Invalidate code (regardless if it's a one time use code)
        '''
        activation_code = ActivationCode.objects.get(code=code)        
        activation_code.force_invalidate()    

    @classmethod
    def create_new_user_from_activation_code(cls, code, username, pwd, pwd_conf):
        '''
        Create new user, validate password, check token
        Return new user on success
        '''
        cls.check_activation_code(code=code)
        cls.compare_passwords(pwd=pwd, pwd_conf=pwd_conf)
        cls.validate_password(pwd=pwd)
        new_user = cls.create_user(username=username,pwd=pwd)
        if new_user:
            cls.invalidate_if_one_time_use_code(code=code)
            return new_user
        else:
            raise Exception("Failed to create new user")
