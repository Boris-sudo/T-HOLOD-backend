from rest_framework import serializers

from .models import Wishes


class WishesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishes
        fields = ('id', 'title', 'count')

    def to_representation(self, instance: Wishes):
        data = super().to_representation(instance)

        data['fridge'] = instance.fridge.name

        return data
