from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import Product
from cart.models import Cart, CartItem

# Create your views here.

# return session by id, 
# or create new one if doesn't exist

def _session_id(request):
    session = request.session.session_key
    if not session:
        session = request.session.create()
    return session


def cart(request):
    
    return render(request, 'store/cart.html')


def add_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except:
        return HttpResponse('No such product')
    
    try:
        cart = Cart.objects.get(cart_id=_session_id(request)) 
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _session_id(request))
        cart.save()
        
    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    
    if is_cart_item_exists:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart_item =CartItem.objects.create(
            cart=cart,
            quantity=1,
            product=product
        )
        cart_item.save()

    return redirect('cart')
