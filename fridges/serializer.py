from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Fridge
from wishes.models import Wishes
from wishes.serializer import WishesSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class FridgeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    owner = UserSerializer(read_only=True)
    admins = UserSerializer(many=True, read_only=True)
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Fridge
        fields = ('id', 'name', 'owner', 'admins', 'members')
    
    def to_representation(self, instance: Fridge):
        data = super().to_representation(instance)

        user = self.context.get('user')

        if user:
            status = "Участник"

            for admin in instance.admins.all():
                if admin == user:
                    status = "Админ"
                    break

            if instance.owner == user:
                status = "Владелец"

            data['status'] = status
        
        data['wishes'] = WishesSerializer(
            Wishes.objects.filter(fridge=instance),
            many = True
        ).data

        return data


class IdSerializer(serializers.Serializer):
    id = serializers.IntegerField()
