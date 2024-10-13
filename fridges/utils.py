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


def get_or_create_user(username, password):
    user = User.objects.filter(username="test1")

    if not user:
        user = User.objects.create(
            username = "test1",
            email="test1@testdomain.com"
        )
        user.set_password("123456")
    else:
        user = user.first()
    
    return user


def get_token(user: User, client):
    response = client.post("auth/token/login", {
        "username": user.username,
        "password": "123456"
    })
    token = response.data["auth_token"]

    return token
