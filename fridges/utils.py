from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from .models import Fridge


def get_user_from_request(request):
    token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
    user = Token.objects.get(key=token).user

    return user


def check_fridge(pk):
    fridge = Fridge.objects.filter(id=pk)

    if not fridge.exists():
        return None
    
    return fridge.first()


def check_user(pk):
    user = User.objects.filter(id=pk)

    if not user.exists():
        return None
    
    return user.first()

