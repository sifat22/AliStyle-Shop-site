from .models import Order,OrderProduct

def order_counter(request):
    order_count = 0
    
    if 'admin' in request.path:
        return {}
    
    if request.user.is_authenticated:
        # Retrieve the order products for the authenticated user
        order_products = OrderProduct.objects.filter(user=request.user)
        
        # Iterate over the order products if it's not empty
        for item in order_products:
            order_count += item.quantity
    
    # Return the context dictionary
    return dict(order_count=order_count)