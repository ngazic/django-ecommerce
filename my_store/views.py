from django.shortcuts import render, HttpResponse
from .models import Product

# Create your views here.

def home(request):
    return render(request, 'index.html')
    
    
def store(request, category_slug=None):
    products = Product.objects.all().filter(is_available=True)
    if category_slug:
        print('if condition')
        products = products.filter(category__slug=category_slug)
    context = {'products': products}
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug=None, product_slug=None):
    return render(request, 'index.html')
