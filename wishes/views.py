from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User

from fridges.utils import get_user_from_request, check_fridge
from .models import Wishes
from .serializer import WishesSerializer
from .utils import check_wishes


class WishesViewSet(ViewSet):
    @action(methods=["POST"], detail=True)
    def add_wish(self, request, pk: int = None):
        user = get_user_from_request(request)

        title = request.data.get('title')
        count = request.data.get('count')

        if not title or not count:
            return Response({
                "error": "some data is not provided" 
            })
        
        fridge = check_fridge(pk)

        if not fridge or not fridge.members.contains(user):
            return Response({
                "error": "no such fridge" 
            })
        
        Wishes.objects.create(
            title = title,
            count = count,
            fridge = fridge
        )

        return Response({
            "message": "ok"
        }, status=201)


    @action(methods=["POST"], detail=True)
    def remove_wish(self, request, pk = None):
        user = get_user_from_request(request)
        
        wish: Wishes = check_wishes(pk)
        print(wish)

        if not wish or not wish.fridge.members.contains(user):
            return Response({
                "error": "cannot remove wish"
            })
        
        wish.delete()

        return Response({
            "message": "ok"
        }, status=201)
