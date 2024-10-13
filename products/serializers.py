from django.contrib.auth.models import User
from rest_framework import serializers
from datetime import datetime
from datetime import timedelta

from .models import Product
from fridges.utils import check_user, check_fridge
from fridges.serializer import FridgeSerializer


class ProductSerializer(serializers.ModelSerializer):
    fridge = FridgeSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ("id", "fridge", "start_date", "end_date", "count", "name")


class ProductCreateSetializer(serializers.Serializer):
    name = serializers.CharField()
    fridge_id = serializers.IntegerField()
    end_date = serializers.DateTimeField()
    count = serializers.IntegerField()

    def save(self, user: User, validated_data: dict):
        fridge = check_fridge(validated_data['fridge_id'])

        if not user or not fridge or not fridge.members.contains(user):
            return None
        
        end_date = datetime.now() + timedelta(days=7) if not validated_data.get('end_date') else validated_data.get('end_date')
        
        product = Product.objects.create(
            name = validated_data['name'],
            fridge = fridge,
            user = user,
            count = validated_data['count'],
            end_date = end_date,
        )

        return product
        

