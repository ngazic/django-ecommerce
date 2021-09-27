from django.shortcuts import render, HttpResponse
from .models import Product

# Create your views here.

def home(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    
    return render(request, 'index.html', context)
    
    
def store(request, category_slug=None):
    products = Product.objects.all().filter(is_available=True)
    if category_slug:
        products = products.filter(category__slug=category_slug)
    context = {'products': products}
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Product.DoesNotExist as e:
        return HttpResponse('Error, product does not exists')
        raise e
        
    context = {
        'product': single_product
        }
    return render(request, 'store/product-detail.html', context)
