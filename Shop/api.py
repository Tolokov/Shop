from Shop.models import Card_Product
from rest_framework import viewsets, permissions
from .serializer import CardSerializer


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card_Product.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CardSerializer
