from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token
# from django.contrib.auth.decorators import user_passes_test


from ..serializers import ShippingAddressSerializer, UserSerializer
from ..models.shippingaddress import ShippingAddress

# class SuperUserCheck(UserPassesTestMixin, APIView):
#     def is_superuser(self):
#         return self.request.user.is_superuser

class ShippingAddressView(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = ShippingAddressSerializer
    def get(self, request):
        """Index ShippingAddress Request"""
        # Get all the mangos:
        # mangos = Mango.objects.all()
        # Filter the mangos by owner, so you can only see your owned mangos
        shippingaddresses = ShippingAddress.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = ShippingAddressSerializer(shippingaddresses, many=True).data
        return Response({ 'shippingaddresses': data })
    
    # Check if user passes a superuser before creating a new product
    # @user_passes_test(lambda u: u.is_superuser)
    def post(self, request):
        """Create ShippingAddress Request"""
        request.data['shippingaddress']['owner'] = request.user.id
        # Serialize/create order
        shippingaddress = ShippingAddressSerializer(data=request.data['shippingaddress'])
        if shippingaddress.is_valid():
            # Save the create product & send a response
            shippingaddress.save()
            return Response(shippingaddress.data, status=status.HTTP_201_CREATED)
         # If the data is not valid, return a response with the errors
        return Response(shippingaddress.errors, status=status.HTTP_400_BAD_REQUEST)

class ShippingAddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show ShippingAddress Request"""
        # Find the order to show
        shippingaddress = get_object_or_404(ShippingAddress, pk=pk)
        # Only show the order that is owned
        if not request.user.id == shippingaddress.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this address')
        
        # Send the data through the serializer to be formatted
        data = ShippingAddressSerializer(shippingaddress).data
        return Response({ 'shippingaddress': data })
    
    def delete(self, request, pk):
        """Delete ShippingAddress Request"""
        shippingaddress = get_object_or_404(ShippingAddress, pk=pk)
        if not request.user.id == shippingaddress.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this address')
        shippingaddress.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def partial_update(self, request, pk):
        """Update ShippingAddress Request"""
        # Remove the owner request object, get the owner key on the data dict and return flase if it doesn't find it. So if it is found remove it
        if request.data['shippingaddress'].get('owner', False):
            del request.data['shippingaddress']['owner']
        
        # Locate the order
        shippingaddress = get_object_or_404(ShippingAddress, pk=pk)
        if not request.user.id == shippingaddress.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this address.')
        
        # add owner to data no that we know this user owns the resource
        request.data['shippingaddress']['owner'] = request.user.id
        # validate updates with serializer
        data = ShippingAddressSerializer(shippingaddress, data=request.data['shippingaddress'])
        if data.is_valid():
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)