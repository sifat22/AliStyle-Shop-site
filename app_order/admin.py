from django.contrib import admin
from.models import Order,Payment,OrderProduct

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display=['order_number','full_name','phone_number','email','city','order_total','tax','status','is_ordered','created_at']
    list_filter=['status','is_ordered']
    search_field=['order_number','phone_number','email']


class OrderProductInline(admin.TabularInline):
    model=OrderProduct
    readonly_fields=('payment','user','product','quantity','product_price','ordered')
    extra =0

admin.site.register(Order,OrderAdmin)
admin.site.register(Payment)
admin.site.register(OrderProduct)
