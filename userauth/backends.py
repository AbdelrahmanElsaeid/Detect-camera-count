# from django.contrib.auth.models import User

# class EmailBackend:
#     def authenticate(self, request, username=None, password=None):
#         try:
#             user = User.objects.get(email=username)
#             if user.check_password(password):
#                 return user
#         except User.DoesNotExist:
#             return None



from django.contrib.auth.backends import ModelBackend
from .models import User

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None
