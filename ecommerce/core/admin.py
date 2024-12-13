from django.contrib import admin
from .models import User, Order

@admin.register(User)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')
    search_fields = ('user__username',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'status', 'total_price')
    list_filter = ('status',)
    search_fields = ('order_id', 'user__username')
