from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token
# from django.contrib.auth.decorators import user_passes_test


from ..serializers import OrderItemSerializer, UserSerializer
from ..models.orderitem import OrderItem

# class SuperUserCheck(UserPassesTestMixin, APIView):
#     def is_superuser(self):
#         return self.request.user.is_superuser

class OrderItemView(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = OrderItemSerializer
    def get(self, request):
        """Index OrderItem Request"""
        # Get all the mangos:
        # mangos = Mango.objects.all()
        # Filter the mangos by owner, so you can only see your owned mangos
        orderitems = OrderItem.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = OrderItemSerializer(orderitems, many=True).data
        return Response({ 'orderitems': data })
    
    # Check if user passes a superuser before creating a new product
    # @user_passes_test(lambda u: u.is_superuser)
    def post(self, request):
        """Create OrderItem Request"""
        request.data['order']['owner'] = request.user.id
        # Serialize/create order
        orderitem = OrderItemSerializer(data=request.data['orderitem'])
        if orderitem.is_valid():
            # Save the create product & send a response
            orderitem.save()
            return Response(orderitem.data, status=status.HTTP_201_CREATED)
         # If the data is not valid, return a response with the errors
        return Response(orderitem.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show OrderItem Request"""
        # Find the order to show
        orderitem = get_object_or_404(OrderItem, pk=pk)
        # Only show the order that is owned
        if not request.user.id == orderitem.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this order item')
        
        # Send the data through the serializer to be formatted
        data = OrderItemSerializer(orderitem).data
        return Response({ 'order': data })
    
    def delete(self, request, pk):
        """Delete OrderItem Request"""
        orderitem = get_object_or_404(OrderItem, pk=pk)
        if not request.user.id == orderitem.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this order item')
        orderitem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def partial_update(self, request, pk):
        """Update OrderItem Request"""
        # Remove the owner request object, get the owner key on the data dict and return flase if it doesn't find it. So if it is found remove it
        if request.data['orderitem'].get('owner', False):
            del request.data['orderitem']['owner']
        
        # Locate the order
        orderitem = get_object_or_404(OrderItem, pk=pk)
        if not request.user.id == orderitem.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this order item')
        
        # add owner to data no that we know this user owns the resource
        request.data['orderitem']['owner'] = request.user.id
        # validate updates with serializer
        data = OrderItemSerializer(orderitem, data=request.data['orderitem'])
        if data.is_valid():
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)