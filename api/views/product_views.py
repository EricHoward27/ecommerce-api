from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token
# from django.contrib.auth.decorators import user_passes_test


from ..serializers import ProductSerializer, UserSerializer
from ..models.product import Product

# class SuperUserCheck(UserPassesTestMixin, APIView):
#     def is_superuser(self):
#         return self.request.user.is_superuser

class ProductView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes=(IsAuthenticated,)
    def get(self, request):
        """Index Product Request"""
        # Get all the mangos:
        # mangos = Mango.objects.all()
        # Filter the mangos by owner, so you can only see your owned mangos
        products = Product.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = ProductSerializer(products, many=True).data
        return Response({ 'products': data })
    
    # Check if user passes a superuser before creating a new product
    # @user_passes_test(lambda u: u.is_superuser)
    def post(self, request):
        """Create Product Request"""
        request.data['product']['owner'] = request.user.id
        # Serialize/create product
        product = ProductSerializer(data=request.data['product'])
        if product.is_valid():
            # Save the create product & send a response
            product.save()
            return Response(product.data, status=status.HTTP_201_CREATED)
         # If the data is not valid, return a response with the errors
        return Response(product.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show Product Request"""
        # Find the product to show
        product = get_object_or_404(Product, pk=pk)
        # Only show the product that is owned
        if not request.user.id == product.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this product')
        
        # Send the data through the serializer to be formatted
        data = ProductSerializer(product).data
        return Response({ 'product': data })
    
    def delete(self, request, pk):
        """Delete Product Request"""
        product = get_object_or_404(Product, pk=pk)
        if not request.user.id == product.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this product')
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def partial_update(self, request, pk):
        """Update Product Request"""
        # Remove the owner request object, get the owner key on the data dict and return flase if it doesn't find it. So if it is found remove it
        if request.data['product'].get('owner', False):
            del request.data['product']['owner']
        
        # Locate the product
        product = get_object_or_404(Product, pk=pk)
        if not request.user.id == product.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this product')
        
        # add owner to data no that we know this user owns the resource
        request.data['product']['owner'] = request.user.id
        # validate updates with serializer
        data = ProductSerializer(product, data=request.data['product'])
        if data.is_valid():
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)