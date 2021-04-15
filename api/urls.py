from django.urls import path
from .views.mango_views import Mangos, MangoDetail
from .views.product_views import ProductView, ProductDetailView
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword
from .views.order_views import OrderView, OrderDetailView
from .views.orderitem_views import OrderItemView, OrderItemDetailView
from .views.review_views import ReviewView, ReviewDetailView
from .views.shippingaddress_views import ShippingAddressView, ShippingAddressDetailView

urlpatterns = [
  	# Restful routing
    path('mangos/', Mangos.as_view(), name='mangos'),
    path('mangos/<int:pk>/', MangoDetail.as_view(), name='mango_detail'),
    path('products/', ProductView.as_view(), name='products'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('orders/', OrderView.as_view(), name='orders'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-item_detail'),
    path('order-item/', OrderItemView.as_view(), name='orders'),
    path('order-item/<int:pk>/', OrderItemDetailView.as_view(), name='order-item_detail'),
    path('reviews/', ReviewView.as_view(), name='reviews'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),
    path('shippingaddresses/', ShippingAddressView.as_view(), name='shippingaddresses'),
    path('shippingaddresses/<int:pk>/', ShippingAddressDetailView.as_view(), name='shippingaddress_detail'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw')
]
