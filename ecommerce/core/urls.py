from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import (
    UserViewSet,
    ProductViewSet,
    CategoryViewSet,
    OrderViewSet,
    OrderItemViewSet,
    ShoppingCartViewSet,
    CartItemViewSet,
    PaymentViewSet,
    ReviewViewSet,
    WishlistViewSet,
    WishlistItemViewSet,
    UserOrdersView,
    UserCartView,
    ProductReviewsView,
    UserWishlistView,
    UserDashboardView
)

# Создание роутера и регистрация всех ViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'shopping-carts', ShoppingCartViewSet)
router.register(r'cart-items', CartItemViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'wishlists', WishlistViewSet)
router.register(r'wishlist-items', WishlistItemViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # API роуты
    path('api/user/<int:user_id>/orders/', UserOrdersView.as_view(), name='user-orders'),
    path('api/user/<int:user_id>/cart/', UserCartView.as_view(), name='user-cart'),
    path('api/product/<int:product_id>/reviews/', ProductReviewsView.as_view(), name='product-reviews'),
    path('api/user/<int:user_id>/wishlist/', UserWishlistView.as_view(), name='user-wishlist'),
    path('api/user/<int:user_id>/dashboard/', UserDashboardView.as_view(), name='user-dashboard'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
]
