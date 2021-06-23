
from rest_framework.views import APIView
from rest_framework import authentication, permissions


class APIAuthView(APIView):
    # TODO: remove basic auth
    authentication_classes = [
            authentication.SessionAuthentication,
            # authentication.BasicAuthentication
        ]
    permission_classes = [permissions.IsAuthenticated]
    def dispatch(self, request, *args, **kwargs):
        return super(__class__, self).dispatch(request, *args,**kwargs)