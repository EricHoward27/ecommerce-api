from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..serializers import ProductSerializer, UserSerializer
from ..models.product import Product

class ProductView(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = ProductSerializer
    def get(self, request):
        """Index request"""
        # Get all the mangos:
        # mangos = Mango.objects.all()
        # Filter the mangos by owner, so you can only see your owned mangos
        products = Product.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = ProductSerializer(products, many=True).data
        return Response({ 'products': data })