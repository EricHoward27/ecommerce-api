from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token
# from django.contrib.auth.decorators import user_passes_test


from ..serializers import OrderSerializer, UserSerializer
from ..models.order import Order

# class SuperUserCheck(UserPassesTestMixin, APIView):
#     def is_superuser(self):
#         return self.request.user.is_superuser

class OrderView(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = OrderSerializer
    def get(self, request):
        """Index Order Request"""
        # Get all the mangos:
        # mangos = Mango.objects.all()
        # Filter the mangos by owner, so you can only see your owned mangos
        orders = Order.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = OrderSerializer(orders, many=True).data
        return Response({ 'orders': data })
    
    # Check if user passes a superuser before creating a new product
    # @user_passes_test(lambda u: u.is_superuser)
    def post(self, request):
        """Create Order Request"""
        request.data['order']['owner'] = request.user.id
        # Serialize/create order
        order = OrderSerializer(data=request.data['order'])
        if order.is_valid():
            # Save the create product & send a response
            order.save()
            return Response(order.data, status=status.HTTP_201_CREATED)
         # If the data is not valid, return a response with the errors
        return Response(order.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show Order Request"""
        # Find the order to show
        order = get_object_or_404(Order, pk=pk)
        # Only show the order that is owned
        if not request.user.id == order.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this order')
        
        # Send the data through the serializer to be formatted
        data = OrderSerializer(order).data
        return Response({ 'order': data })
    
    def delete(self, request, pk):
        """Delete Order Request"""
        order = get_object_or_404(Order, pk=pk)
        if not request.user.id == order.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this order')
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def partial_update(self, request, pk):
        """Update Order Request"""
        # Remove the owner request object, get the owner key on the data dict and return flase if it doesn't find it. So if it is found remove it
        if request.data['order'].get('owner', False):
            del request.data['order']['owner']
        
        # Locate the order
        order = get_object_or_404(Order, pk=pk)
        if not request.user.id == order.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this order')
        
        # add owner to data no that we know this user owns the resource
        request.data['order']['owner'] = request.user.id
        # validate updates with serializer
        data = OrderSerializer(order, data=request.data['order'])
        if data.is_valid():
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)