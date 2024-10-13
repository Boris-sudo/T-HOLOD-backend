from django.test import TestCase
from django.urls import path, include, reverse
from rest_framework.routers import SimpleRouter
from django.contrib.auth.models import User

from .views import FridgeViewSet
from .utils import get_token, get_or_create_user


class FridgeTests(TestCase):
    router = SimpleRouter()
    router.register('fridges', FridgeViewSet, basename="fridges")
    urlpatterns = [
        path("/", include(router.urls)),
        path(r'auth/', include('djoser.urls')),
        path(r'auth/', include('djoser.urls.authtoken')),
    ]

    def test_create_fridge(self):
        user = get_or_create_user("test1", 123456)
        token = get_token(user, self.client)

        response_fridge = self.client.post(
            reverse("fridges-create"),
            data = {
                "name": "test_fridge"
            },
            headers = {
                "Authorization": "Token" + token
            }
        )

        self.assertEqual(response_fridge.status_code, 200)


