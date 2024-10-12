from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from .models import Fridge
from .serializer import FridgeSerializer
from .utils import get_user_from_request, check_fridge, check_user


class FridgeViewSet(ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def validate_users(self, request, pk):
        user = get_user_from_request(request)

        fridge = check_fridge(pk)

        if not fridge:
            return Response({
                "error": "no such fridge"
            }, status=404)
        
        user_id = request.data.get("id")

        if user_id == user.id:
            return Response({
                "error": "you cannot add yourself!"
            }, status=403)
        
        user_add = check_user(user_id)

        if not user_add:
            return Response({
                "error": "no such user!"
            }, status=403)
        
        if not fridge.owner == user and not fridge.admins.contains(user):
            return Response({
                "error": "You hasn't permissions to do that!"
            })
        
        return fridge, user_add, user

    def list(self, request):
        user = get_user_from_request(request)

        fridges = Fridge.objects.filter(
            members__in = [user]
        )

        return Response(FridgeSerializer(fridges, many=True, context={"user": user}).data)

    def retrieve(self, request, pk=None):
        user = get_user_from_request(request)

        fridge = check_fridge(pk)

        if not fridge or not fridge.members.contains(user):
            return Response(
                {
                    "error": "no such fridge!"
                },
                status=404
            )
        
        return Response(FridgeSerializer(fridge, context={"user": user}).data)

    @swagger_auto_schema(operation_description="""
        Создает холодильник. Прнимает body параметр, состоящии из name: str - название холодильника
    """)
    def create(self, request):
        user = get_user_from_request(request)
        name = request.data.get('name')

        if not name:
            return Response(
                {"error": "name is not provided!"},
                status = 400
            )
        
        fridge = Fridge.objects.create(owner=user, name=name)
        fridge.members.add(user)
        fridge.admins.add(user)

        return Response(FridgeSerializer(instance=fridge, context={"user": user}).data)

    @swagger_auto_schema(operation_description="""
        Удаляет холодильник. Прнимает path параметр - id: int
    """)
    @action(methods=["DELETE"], detail=True)
    def delete_fridge(self, request, pk=None):
        user = get_user_from_request(request)

        fridge = Fridge.objects.filter(id=pk)

        if not fridge.exists():
            return Response({
                "error": "no such fridge"
            }, status=404)
        
        fridge = fridge.first()

        if fridge.owner == user:
            fridge.delete()
        else:
            fridge.admins.remove(user)
            fridge.members.remove(user)
        
        return Response({
            "message": "deleted"
        })

    
    @swagger_auto_schema(operation_description="""
        Добавляет пользователя. Прнимает path параметр - id: int пользователя
    """)
    @action(methods=["POST"], detail=True)
    def add_member(self, request, pk=None):
        validate = self.validate_users(request, pk)

        if isinstance(validate, Response):
            return validate
        
        fridge, user_add, user = validate
        
        fridge.members.add(user_add)

        return Response({
            "message": "ok"
        })

    @swagger_auto_schema(operation_description="""
        Удаляет пользователя. Прнимает path параметр - id: int пользователя
    """)
    @action(methods=["DELETE"], detail=True)
    def remove_member(self, request, pk=None):
        validate = self.validate_users(request, pk)

        if isinstance(validate, Response):
            return validate
        
        fridge, user_add, user = validate

        if not fridge.owner == user and not fridge.admins.contains(user):
            return Response({
                "error": "You hasn't permissions to do that!"
            })

        if fridge.members.contains(user_add):
            fridge.members.remove(user_add)
        
        if fridge.admins.contains(user_add):
            fridge.admins.remove(user_add)

        return Response({
            "message": "ok"
        })
    
    @action(methods=["POST"], detail=True)
    def add_admin(self, request, pk=None):
        validate = self.validate_users(request, pk)

        if isinstance(validate, Response):
            return validate
        
        fridge, user_add, user = validate

        if not fridge.owner == user:
            return Response({
                "error": "You hasn't permissions to do that!"
            })
        
        if not fridge.members.contains(user_add):
            return Response({
                "error": "no such user!"
            })
        
        fridge.admins.add(user_add)

        return Response({
            "message": "ok"
        })
    
    @action(methods=["DELETE"], detail=True)
    def remove_admin(self, request, pk=None):
        validate = self.validate_users(request, pk)

        if isinstance(validate, Response):
            return validate
        
        fridge, user_add, user = validate

        if not fridge.owner == user:
            return Response({
                "error": "You hasn't permissions to do that!"
            })
        
        if not fridge.members.contains(user_add):
            return Response({
                "error": "no such user!"
            })
        
        fridge.admins.remove(user_add)

        return Response({
            "message": "ok"
        })

