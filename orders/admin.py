from django.contrib import admin
from .models import Order, OrderItem, Subscription, Subscriptions


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'paid', 'created',
                    'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(Subscriptions)
admin.site.register(Subscription)

