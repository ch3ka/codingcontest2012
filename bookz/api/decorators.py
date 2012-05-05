from functools import wraps
from api.models import Apikey
from api.exceptions import ApiException
from django.http import HttpResponse
import settings

def booleanapicall(func, key_required=True):
    """wraps function to check for exception.
        if keyrequired is True (default), then also check for
        valid API key.
        returns 'False' when Exception occured, 'True' otherwise"""
    @wraps(func)
    def check_exception(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception:
            if settings.DEBUG: 
                raise
            return HttpResponse('False')
        else:
            return HttpResponse('True')
    return keyrequired(check_exception) if key_required else check_exception

def keyrequired(func):
    """checks for active API key """
    @wraps(func)
    def with_keycheck(*args, **kwargs):
        try:
            api = Apikey.objects.get(key=kwargs['apikey'])
            del kwargs['apikey']
        except Apikey.DoesNotExist:
            raise ApiException("No API Key")
        if not api.active:
            raise ApiException("API Key not active")
        return func(*args, user=api.user, **kwargs)
    return with_keycheck


