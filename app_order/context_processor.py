from .models import Order,OrderProduct

def order_counter(request):
    order_count = 0
    if 'admin' in request.path:
        return{}
    else:
        if request.user.is_authenticated:
            order = OrderProduct.objects.filter(user = request.user)       
        for order in order:
            order_count += order.quantity
                
    return dict(order_count=order_count)