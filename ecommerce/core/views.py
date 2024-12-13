from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from .models import User, Product, Category, Order, OrderItem, ShoppingCart, CartItem, Payment, Review, Wishlist, WishlistItem
from .serializers import UserSerializer, ProductSerializer, CategorySerializer, OrderSerializer, OrderItemSerializer, ShoppingCartSerializer, CartItemSerializer, PaymentSerializer, ReviewSerializer, WishlistSerializer, WishlistItemSerializer
from django.http import JsonResponse
from tasks import send_email_task
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer


class WishlistItemViewSet(viewsets.ModelViewSet):
    queryset = WishlistItem.objects.all()
    serializer_class = WishlistItemSerializer


def get_orders_with_details(user_id):
    orders = Order.objects.filter(user_id=user_id) \
        .select_related('user') \
        .prefetch_related('items__product')
    return orders


def get_cart_with_items(user_id):
    cart = ShoppingCart.objects.filter(user_id=user_id) \
        .select_related('user') \
        .prefetch_related('items__product') \
        .first()
    return cart


def get_product_reviews(product_id):
    reviews = Review.objects.filter(product_id=product_id) \
        .select_related('user') \
        .all()
    return reviews


def get_wishlist_with_items(user_id):
    wishlist = Wishlist.objects.filter(user_id=user_id) \
        .prefetch_related('items__product') \
        .first()
    return wishlist


def user_dashboard(request):
    user_id = request.user.id
    orders = get_orders_with_details(user_id)
    cart = get_cart_with_items(user_id)
    wishlist = get_wishlist_with_items(user_id)

    return render(request, 'user_dashboard.html', {
        'orders': orders,
        'cart': cart,
        'wishlist': wishlist,
    })


class UserOrdersView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        cache_key = f'user_{user_id}_orders'
        cached_orders = cache.get(cache_key)

        if cached_orders:
            return Response(cached_orders, status=status.HTTP_200_OK)

        try:
            orders = get_orders_with_details(user_id)
            serializer = OrderSerializer(orders, many=True)
            cache.set(cache_key, serializer.data, timeout=60*15)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'detail': 'Orders not found'}, status=status.HTTP_404_NOT_FOUND)


class UserCartView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        cache_key = f'user_{user_id}_cart'
        cached_cart = cache.get(cache_key)

        if cached_cart:
            return Response(cached_cart, status=status.HTTP_200_OK)

        try:
            cart = get_cart_with_items(user_id)
            if cart is None:
                return Response({'detail': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = ShoppingCartSerializer(cart)
            cache.set(cache_key, serializer.data, timeout=60*15)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ShoppingCart.DoesNotExist:
            return Response({'detail': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)


class ProductReviewsView(APIView):
    def get(self, request, product_id, *args, **kwargs):
        cache_key = f'product_{product_id}_reviews'
        cached_reviews = cache.get(cache_key)

        if cached_reviews:
            return Response(cached_reviews, status=status.HTTP_200_OK)

        try:
            reviews = get_product_reviews(product_id)
            serializer = ReviewSerializer(reviews, many=True)
            cache.set(cache_key, serializer.data, timeout=60*15)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Review.DoesNotExist:
            return Response({'detail': 'Reviews not found'}, status=status.HTTP_404_NOT_FOUND)


class UserWishlistView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        cache_key = f'user_{user_id}_wishlist'
        cached_wishlist = cache.get(cache_key)

        if cached_wishlist:
            return Response(cached_wishlist, status=status.HTTP_200_OK)

        try:
            wishlist = get_wishlist_with_items(user_id)
            if wishlist is None:
                return Response({'detail': 'Wishlist not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = WishlistSerializer(wishlist)
            cache.set(cache_key, serializer.data, timeout=60*15)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Wishlist.DoesNotExist:
            return Response({'detail': 'Wishlist not found'}, status=status.HTTP_404_NOT_FOUND)


class UserDashboardView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        cache_key = f'user_{user_id}_dashboard'
        cached_dashboard = cache.get(cache_key)

        if cached_dashboard:
            return Response(cached_dashboard, status=status.HTTP_200_OK)

        try:
            orders = get_orders_with_details(user_id)
            cart = get_cart_with_items(user_id)
            wishlist = get_wishlist_with_items(user_id)

            data = {
                'orders': orders,
                'cart': cart,
                'wishlist': wishlist,
            }

            cache.set(cache_key, data, timeout=60*15)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def send_email_view(request):
    recipient_email = request.GET.get('email', 'user@example.com')
    send_email_task.delay(recipient_email)
    return JsonResponse({'status': 'Email task added to queue'})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'templates/register.html', {'form': form})

from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='10/m', block=True)
def my_view(request):
    return JsonResponse({'message': 'Success'})