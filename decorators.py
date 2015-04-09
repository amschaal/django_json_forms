from models import Response
from django.http import HttpResponseForbidden 

from django.conf import settings
from django.utils.module_loading import import_string

def is_admin(user,response):
    return user.is_superuser
def allow_all(user,response):
    return True
class download_permission(object):
    def __init__(self, response_id_param='pk'):
        self.response_id_param  = response_id_param
        perm_function_string = getattr(settings,'DJANGO_JSON_FORMS_DOWNLOAD_PERMISSIONS','django_json_forms.decorators.is_admin')
        self.permission_function = import_string(perm_function_string)
    def __call__(self, f):
        def wrapped_f(*args,**kwargs):
#             print args
#             print kwargs
            response = Response.objects.get(id=kwargs[self.response_id_param])
            request = args[0]
            if not self.permission_function(request.user,response):
                return HttpResponseForbidden('Permission denied')
            return f(*args,**kwargs)
        return wrapped_f