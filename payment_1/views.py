from django.shortcuts import render , redirect
from cart.cart import Cart
from django.contrib import messages

from payment_1.forms import ShippingForm
from payment_1.models import ShippingAddress



def billing_info(request):

    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
        
    if request.user.is_authenticated:
        return render(request , 'payment/billing_info.html' , {'cart_products':cart_products , 'quantities':quantities , 'totals':totals , 'shipping_info':request.POST})
        
    else:
        pass
        
    shipping_form=request.POST
            
    return render(request , 'payment/billing_info.html' , {'cart_products':cart_products , 'quantities':quantities , 'totals':totals , 'shipping_form':shipping_form})
    
    
        
        

def checkout(request):
     # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    
    if request.user.is_authenticated:
        # Get current User's Shipping Info
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # Get User's Shipping Form
        shipping_form=ShippingForm(request.POST or None , instance = shipping_user)
        
        return render(request , 'payment/checkout.html' , {'cart_products':cart_products , 'quantities':quantities , 'totals':totals , 'shipping_form':shipping_form})
    else:
        shipping_form=ShippingForm(request.POST or None)
        return render(request , 'payment/checkout.html' , {'cart_products':cart_products , 'quantities':quantities , 'totals':totals , 'shipping_form':shipping_form})
    
# def checkout(request):
#     # Get the cart
#     cart = Cart(request)
#     cart_products = cart.get_prods
#     quantities = cart.get_quants
#     totals = cart.cart_total()
    
#     if request.user.is_authenticated:
#         # Get current User's Shipping Info if user is authenticated
        
#         try:
#             shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
#             shipping_form = ShippingForm(instance=shipping_user)
#             if shipping_user.shipping_full_name:
#                 return render(request, 'payment/checkout.html', {
#                 'cart_products': cart_products,
#                 'quantities': quantities,
#                 'totals': totals,
#                 'shipping_user': shipping_user
#             })
#             else:
#                 shipping_form = ShippingForm()
            
#         except ShippingAddress.DoesNotExist:
#             shipping_form = ShippingForm()
            
#     else:
#         shipping_form = ShippingForm(request.POST)

#     return render(request, 'payment/checkout.html', {
#         'cart_products': cart_products,
#         'quantities': quantities,
#         'totals': totals,
#         'shipping_form': shipping_form
#     })

def payment_success(request): 
    return render(request , 'payment/payment_success.html' , {})


