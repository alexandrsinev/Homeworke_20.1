from django.shortcuts import render

from catalog.models import Product


# Create your views here.
def home_page(request):
    products_list = Product.objects.all()
    context = {'products': products_list}
    return render(request, 'catalog/home.html', context)


def contacts_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'{name} {phone} {message}')
    return render(request, 'catalog/contacts.html')


def product_page(request, pk):
    product = Product.objects.get(pk=pk)
    context = {'product': product}
    return render(request, 'catalog/product.html', context)
