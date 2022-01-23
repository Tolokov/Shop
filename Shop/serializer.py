from rest_framework import serializers
from Shop.models import Card_Product


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card_Product
        fields = '__all__'
