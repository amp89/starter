
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from django.http import HttpResponseForbidden
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from logger import logger
from django.shortcuts import redirect

class SuperUserView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super(__class__, self).dispatch(request, *args, **kwargs)
        else:
            logger.error(f"Attempt by non superuser to access superuser data: {request.user.id}:{request.user.username}")
            return redirect("ui:home")
            

class APIAuthView(APIView):
    # TODO: remove basic auth
    authentication_classes = [
            authentication.SessionAuthentication,
            # authentication.BasicAuthentication
        ]
    permission_classes = [permissions.IsAuthenticated]
    def dispatch(self, request, *args, **kwargs):
        return super(__class__, self).dispatch(request, *args,**kwargs)