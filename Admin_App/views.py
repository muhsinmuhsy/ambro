from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
from Admin_App.models import *
from django.core.exceptions import ValidationError
# Create your views here.


@login_required(login_url='/U_Auth/admin_login/')
def dashboard(request):
    return render(request, 'Admin/dashboard.html')


def product_list(request):
    products = Product.objects.all()
    return render(request, 'Admin/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'Admin/product_detail.html', {'product': product})

def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        price = request.POST.get('price')
        description = request.POST.get('description')

        try:
            product = Product.objects.create(name=name, image=image, price=price, description=description)
            return redirect('product_list')
        except ValidationError as e:
            error_message = str(e)
    else:
        error_message = None

    return render(request, 'Admin/add_product.html', {'error_message': error_message})

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        price = request.POST.get('price')
        description = request.POST.get('description')

        try:
            product.name = name
            if image:
                product.image = image
            product.price = price
            product.description = description
            product.save()
            return redirect('product_list')
        except ValidationError as e:
            error_message = str(e)
    else:
        error_message = None

    return render(request, 'Admin/edit_product.html', {'product': product, 'error_message': error_message})

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    product.delete()
    return redirect('product_list')
    

