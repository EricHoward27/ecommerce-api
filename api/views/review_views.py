from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token
# from django.contrib.auth.decorators import user_passes_test


from ..serializers import ReviewSerializer, UserSerializer
from ..models.review import Review

# class SuperUserCheck(UserPassesTestMixin, APIView):
#     def is_superuser(self):
#         return self.request.user.is_superuser

class ReviewView(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = ReviewSerializer
    def get(self, request):
        """Index Review Request"""
        # Get all the mangos:
        # mangos = Mango.objects.all()
        # Filter the mangos by owner, so you can only see your owned mangos
        reviews = Review.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = ReviewSerializer(reviews, many=True).data
        return Response({ 'reviews': data })
    
    # Check if user passes a superuser before creating a new product
    # @user_passes_test(lambda u: u.is_superuser)
    def post(self, request):
        """Create Review Request"""
        request.data['review']['owner'] = request.user.id
        # Serialize/create order
        review = ReviewSerializer(data=request.data['review'])
        if review.is_valid():
            # Save the create product & send a response
            review.save()
            return Response(review.data, status=status.HTTP_201_CREATED)
         # If the data is not valid, return a response with the errors
        return Response(review.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show Review Request"""
        # Find the order to show
        review = get_object_or_404(Review, pk=pk)
        # Only show the order that is owned
        if not request.user.id == review.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this review')
        
        # Send the data through the serializer to be formatted
        data = ReviewSerializer(review).data
        return Response({ 'review': data })
    
    def delete(self, request, pk):
        """Delete Review Request"""
        review = get_object_or_404(Review, pk=pk)
        if not request.user.id == review.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this review')
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def partial_update(self, request, pk):
        """Update Review Request"""
        # Remove the owner request object, get the owner key on the data dict and return flase if it doesn't find it. So if it is found remove it
        if request.data['review'].get('owner', False):
            del request.data['review']['owner']
        
        # Locate the order
        review = get_object_or_404(Review, pk=pk)
        if not request.user.id == review.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this review.')
        
        # add owner to data no that we know this user owns the resource
        request.data['review']['owner'] = request.user.id
        # validate updates with serializer
        data = ReviewSerializer(review, data=request.data['review'])
        if data.is_valid():
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)