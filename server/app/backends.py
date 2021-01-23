from django.contrib.auth.backends import ModelBackend
from .models import User
from django.contrib.auth.hashers import check_password


class CustomBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        user_id = kwargs['username']
        password = kwargs['password']
        print(kwargs, request)
        user_type = hasattr(request, 'data') and request.data.get('type', None) or""
        
        try:
            user = User.objects.get(username=user_id)
            type_switch = {'funder':1, 'owner':2, 'auth':3}
            print("2)", user.check_password(password),  user_type,user.user_type, user.user_type  == user_type)
            if user.check_password(password) and (not user_type or (user.user_type and user.user_type  == type_switch.get(user_type))):
                print('user good', user)
                return user
        except User.DoesNotExist:
            pass