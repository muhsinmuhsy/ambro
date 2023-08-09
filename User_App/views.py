from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.sessions.models import Session
from Admin_App.models import Product
from User_App.models import *
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Cart, CartItem, Order
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from decimal import Decimal


# Create your views here.

def home(request):
    products = Product.objects.all()
    # if request.method == 'POST':
    #     product_id = request.POST.get('product_id')
    #     product = get_object_or_404(Product, pk=product_id)
    #     session_key = request.session.session_key
    #     cart, created = Cart.objects.get_or_create(user_session_key=session_key)
    #     cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
        
    #     if not item_created:
    #         cart_item.quantity += 1
    #         cart_item.save()
    #         return redirect('home') 

    user_session_key = request.session.session_key
    try:
        cart = Cart.objects.get(user_session_key=user_session_key)
        cart_quantity_total = sum(item.quantity for item in cart.cartitem_set.all())
    except Cart.DoesNotExist:
        cart_quantity_total = 0
    
    context = {
        'cart_quantity_total' : cart_quantity_total,
        'products': products
    }

    return render(request, 'User/home.html', context)



def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
     # Assuming you are using user sessions and the session key to identify the cart
    user_session_key = request.session.session_key
    try:
        cart = Cart.objects.get(user_session_key=user_session_key)
        cart_quantity_total = sum(item.quantity for item in cart.cartitem_set.all())
    except Cart.DoesNotExist:
        cart_quantity_total = 0
    return render(request, 'User/product_view.html', {'product': product, 'cart_quantity_total' : cart_quantity_total})


# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     session_key = request.session.session_key
#     cart, created = Cart.objects.get_or_create(user_session_key=session_key)

#     cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

#     if not item_created:
#         cart_item.quantity += 1
#         cart_item.save()

#     return redirect('product_view', pk=product.id)




# def add_to_cart_one(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     session_key = request.session.session_key
#     cart, created = Cart.objects.get_or_create(user_session_key=session_key)
#     cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
#     if not item_created:
#         cart_item.quantity += 1
#         cart_item.save()

#     return redirect('home') 






def add_to_cart_one(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Ensure that the user has a session key (create one if it doesn't exist)
    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key
    cart, created = Cart.objects.get_or_create(user_session_key=session_key)

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f"Cart Added Succes fully")
    return redirect('home')


    
def add_to_cart_two(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Ensure that the user has a session key (create one if it doesn't exist)
    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key
    cart, created = Cart.objects.get_or_create(user_session_key=session_key)

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"Cart Added Succes fully")
    return redirect('product_view', pk=product.id)


def cart_items_view(request):
    session_key = request.session.session_key
    cart = Cart.objects.filter(user_session_key=session_key).first()

    # calculation subtotal without tax
    if cart:
        sub_total_price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())
        cart_items = CartItem.objects.filter(cart=cart)
    else:
        sub_total_price = 0
        cart_items = None

    # if cart:
    #     cart_items = CartItem.objects.filter(cart=cart)
    #     total_price = sum(Decimal(item.product.price) * item.quantity for item in cart_items)
    #     tax = Decimal('0.05') * total_price  # Calculate 5% tax
    #     total_price += tax  # Add tax to the total price
    # else:
    #     total_price = 0
    #     cart_items = None

    if cart:
        cart_items = CartItem.objects.filter(cart=cart)
        total_price = sum(Decimal(item.product.price) * item.quantity for item in cart_items)
        tax = Decimal('0.05') * total_price  # Calculate 5% tax
        total_price += tax  # Add tax to the total price
        
        # Format the total_price and tax to have two decimal places
        total_price = total_price.quantize(Decimal('0.00'))
        tax = tax.quantize(Decimal('0.00'))
    else:
        total_price = Decimal('0.00')
        tax = Decimal('0.00')
        cart_items = None

        
    if cart:
        cart_items = CartItem.objects.filter(cart=cart)
        # calculation product one buy one
        for item in cart_items:
            item.subtotal = item.product.price * item.quantity
    else:
        cart_items = []

    return render(request, 'User/cart_items.html', {'cart_items': cart_items, 'total_price' : total_price, 'sub_total_price' : sub_total_price})



def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id)
    item.quantity += 1
    item.save()
    return redirect('cart_items_view')

def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    return redirect('cart_items_view')





# from django.http import JsonResponse

# def update_cart_item(request, cart_item_id):
#     cart_item = get_object_or_404(CartItem, id=cart_item_id)
    
#     if request.method == 'POST':
#         action = request.POST.get('action')
#         if action == 'increment':
#             cart_item.quantity += 1
#             cart_item.save()
#         elif action == 'decrement':
#             if cart_item.quantity > 1:
#                 cart_item.quantity -= 1
#                 cart_item.save()
#             else:
#                 # If the quantity is 1, set it to one (do not delete the item)
#                 cart_item.quantity = 1
#                 cart_item.save()

#         return JsonResponse({'success': True, 'new_quantity': cart_item.quantity})
#     else:
#         return JsonResponse({'success': False})



# def update_cart_item(request, cart_item_id):
#     cart_item = get_object_or_404(CartItem, id=cart_item_id)
    
#     if request.method == 'POST':
#         action = request.POST.get('action')
#         if action == 'increment':
#             cart_item.quantity += 1
#             cart_item.save()
#         elif action == 'decrement':
#             if cart_item.quantity > 1:
#                 cart_item.quantity -= 1
#                 cart_item.save()

#         return JsonResponse({'success': True, 'new_quantity': cart_item.quantity})
#     else:
#         return JsonResponse({'success': False})




# from django.shortcuts import render, redirect
# from .models import Cart, CartItem, Order

# def checkout(request):
#     if request.method == 'POST':
#         # Check if the request method is POST (i.e., form submission after checkout)

#         # Get the user's cart using the session key
#         session_key = request.session.session_key
#         cart = Cart.objects.filter(user_session_key=session_key).first()

#         # Extract the form data from the POST request
#         name = request.POST.get('name')
#         address = request.POST.get('address')
#         mobile_number = request.POST.get('mobile_number')
#         whatsapp_number = request.POST.get('whatsapp_number')

#         # Calculate the total price of all the cart items
#         total_price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())

        

#         # Create a new order with the provided form data and the cart's total price
#         order = Order.objects.create(cart=cart, name=name, address=address,
#                                      mobile_number=mobile_number, whatsapp_number=whatsapp_number,
#                                      total_price=total_price)

#         # # Clear the cart after checkout (optional, depends on your requirements)
#         # cart.cartitem_set.all().delete()

#         # Redirect to a success page or order confirmation page, passing the order ID
#         return redirect('order_confirmation', order_id=order.id)

        
#     else:
#         # If the request method is not POST (e.g., initial loading of the checkout page)

#         # Get the user's cart using the session key
#         session_key = request.session.session_key
#         cart = Cart.objects.filter(user_session_key=session_key).first()

#         # Retrieve all the cart items associated with the cart
#         if cart:
#             cart_items = CartItem.objects.filter(cart=cart)
#         else:
#             cart_items = None

#         # Render the checkout page with the cart items for display
#         return render(request, 'User/checkout.html', {'cart_items': cart_items})




# # Import the necessary libraries for URL encoding and redirect
# from urllib.parse import quote
# from django.shortcuts import render, redirect

# def checkout(request):
#     if request.method == 'POST':
#         # Check if the request method is POST (i.e., form submission after checkout)

#         # Get the user's cart using the session key
#         session_key = request.session.session_key
#         cart = Cart.objects.filter(user_session_key=session_key).first()

#         # Extract the form data from the POST request
#         name = request.POST.get('name')
#         address = request.POST.get('address')
#         mobile_number = request.POST.get('mobile_number')
#         whatsapp_number = request.POST.get('whatsapp_number')

#         # Calculate the total price of all the cart items
#         total_price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())

#         # Create a new order with the provided form data and the cart's total price
#         order = Order.objects.create(cart=cart, name=name, address=address,
#                                      mobile_number=mobile_number, whatsapp_number=whatsapp_number,
#                                      total_price=total_price)

#         # Prepare the order details for WhatsApp message
#         order_details = f"Order ID: {order.id}\nName: {name}\nAddress: {address}\nMobile Number: {mobile_number}\nTotal Price: {total_price}"

#         # URL-encode the order_details using urllib.parse.quote
#         order_details_encoded = quote(order_details)

#         # Construct the WhatsApp URL with order details
#         whatsapp_url = f"https://api.whatsapp.com/send?phone=+919895291631&text={order_details_encoded}"

#         # Redirect the user to WhatsApp with the order details pre-filled
#         return redirect(whatsapp_url)

#     else:
#         # If the request method is not POST (e.g., initial loading of the checkout page)

#         # Get the user's cart using the session key
#         session_key = request.session.session_key
#         cart = Cart.objects.filter(user_session_key=session_key).first()

#         # Retrieve all the cart items associated with the cart
#         if cart:
#             cart_items = CartItem.objects.filter(cart=cart)
#         else:
#             cart_items = None

#         # Render the checkout page with the cart items for display
#         return render(request, 'User/checkout.html', {'cart_items': cart_items})


# # Import the necessary libraries for URL encoding and redirect
# from urllib.parse import quote
# from django.shortcuts import render, redirect

# def checkout(request):
#     if request.method == 'POST':
#         # Check if the request method is POST (i.e., form submission after checkout)

#         # Get the user's cart using the session key
#         session_key = request.session.session_key
#         cart = Cart.objects.filter(user_session_key=session_key).first()

#         # Extract the form data from the POST request
#         name = request.POST.get('name')
#         address = request.POST.get('address')
#         mobile_number = request.POST.get('mobile_number')
#         whatsapp_number = request.POST.get('whatsapp_number')

#         # Calculate the total price of all the cart items
#         total_price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())

#         # Create a new order with the provided form data and the cart's total price
#         order = Order.objects.create(cart=cart, name=name, address=address,
#                                      mobile_number=mobile_number, whatsapp_number=whatsapp_number,
#                                      total_price=total_price)

        

#         # Prepare the order details for WhatsApp message, including cart items
#         order_details = "Order Details:\n"
#         for cart_item in cart.cartitem_set.all():
#             order_details += f"Product: {cart_item.product.name}, Quantity: {cart_item.quantity}, Price: {cart_item.product.price}\n"

#         order_details += f"\nTotal Price: {total_price}\n"
#         order_details += f"Name: {name}\n"
#         order_details += f"Address: {address}\n"
#         order_details += f"Mobile Number: {mobile_number}\n"

#         # URL-encode the order_details using urllib.parse.quote
#         order_details_encoded = quote(order_details)

#         # Construct the WhatsApp URL with order details
#         whatsapp_url = f"https://api.whatsapp.com/send?phone=+919895291631&text={order_details_encoded}"

#         # Redirect the user to WhatsApp with the order details pre-filled
#         return redirect(whatsapp_url)

#     else:
#         # If the request method is not POST (e.g., initial loading of the checkout page)

#         # Get the user's cart using the session key
#         session_key = request.session.session_key
#         cart = Cart.objects.filter(user_session_key=session_key).first()

#         # Retrieve all the cart items associated with the cart
#         if cart:
#             cart_items = CartItem.objects.filter(cart=cart)
#         else:
#             cart_items = None

#         # Render the checkout page with the cart items for display
#         return render(request, 'User/checkout.html', {'cart_items': cart_items})


# Import the necessary libraries for URL encoding and redirect
from urllib.parse import quote
from django.shortcuts import render, redirect

def checkout(request):
    session_key = request.session.session_key
    cart = Cart.objects.filter(user_session_key=session_key).first()

    if cart:
        cart_items = CartItem.objects.filter(cart=cart)
        total_price = sum(Decimal(item.product.price) * item.quantity for item in cart_items)
        tax = Decimal('0.05') * total_price  # Calculate 5% tax
        total_price += tax  # Add tax to the total price
        
        # Format the total_price and tax to have two decimal places
        total_price = total_price.quantize(Decimal('0.00'))
        tax = tax.quantize(Decimal('0.00'))
    else:
        total_price = Decimal('0.00')
        tax = Decimal('0.00')
        cart_items = None

    # calculation subtotal without tax
    if cart:
        sub_total_price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())
        cart_items = CartItem.objects.filter(cart=cart)
    else:
        sub_total_price = 0
        cart_items = None
    
    if request.method == 'POST':
        # Check if the request method is POST (i.e., form submission after checkout)

        # Get the user's cart using the session key
        session_key = request.session.session_key
        cart = Cart.objects.filter(user_session_key=session_key).first()

        if cart:
            cart_items = CartItem.objects.filter(cart=cart)
            total_price = sum(Decimal(item.product.price) * item.quantity for item in cart_items)
            tax = Decimal('0.05') * total_price  # Calculate 5% tax
            total_price += tax  # Add tax to the total price
            
            # Format the total_price and tax to have two decimal places
            total_price = total_price.quantize(Decimal('0.00'))
            tax = tax.quantize(Decimal('0.00'))
        else:
            total_price = Decimal('0.00')
            tax = Decimal('0.00')
            cart_items = None

        # calculation subtotal without tax
        if cart:
            sub_total_price = sum(item.product.price * item.quantity for item in cart.cartitem_set.all())
            cart_items = CartItem.objects.filter(cart=cart)
        else:
            sub_total_price = 0
            cart_items = None

        # Extract the form data from the POST request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        address = request.POST.get('address')
        address_two = request.POST.get('address_two')
        town = request.POST.get('town')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        order_note = request.POST.get('order_note')
        


        # Create a new order with the provided form data and the cart's total price
        order = Order.objects.create(cart=cart,
                                    first_name=first_name,
                                    last_name=last_name,
                                    email=email,
                                    mobile_number=mobile_number,
                                    address=address,
                                    address_two=address_two,
                                    town=town,
                                    state=state,
                                    zip=zip_code,
                                    order_note=order_note,
                                    )      

        # Prepare the order details for WhatsApp message, including cart items
        order_details = "Order Details:\n"
        for cart_item in cart.cartitem_set.all():
            item_total = cart_item.product.price * cart_item.quantity
            order_details += f"*Product:* {cart_item.product.name}, *Price:* {cart_item.product.price}, *Quantity:* {cart_item.quantity}, *Total:* {item_total} \n"

        


        order_details += f"\n----------------------\n"
        order_details += f"\n*Sub Total Price*: {sub_total_price}\n"
        order_details += f"*Tax*: {'5%'}\n"
        order_details += f"*Total Price*: {total_price}\n"
        order_details += f"----------------------\n"

        

        order_details += f"*Name*: {first_name}, {last_name}\n"
        order_details += f"*Address*: {email}\n"
        order_details += f"*Mobile Number*: {mobile_number}\n"             
        order_details += f"*Address*: {address}\n"
        order_details += f"{address_two}\n"
        order_details += f"*Town*: {town}\n"
        order_details += f"*Status*: {state}\n"
        order_details += f"*Zip Code*: {zip_code}\n"



        
        

        # URL-encode the order_details using urllib.parse.quote
        order_details_encoded = quote(order_details)

        # Construct the WhatsApp URL with order details
        whatsapp_url = f"https://api.whatsapp.com/send?phone=+919614900400&text={order_details_encoded}"

        # Redirect the user to WhatsApp with the order details pre-filled
        return redirect(whatsapp_url)

    else:
        # If the request method is not POST (e.g., initial loading of the checkout page)

        # Get the user's cart using the session key
        session_key = request.session.session_key
        cart = Cart.objects.filter(user_session_key=session_key).first()

        # Retrieve all the cart items associated with the cart
        if cart:
            cart_items = CartItem.objects.filter(cart=cart)
            # calculation product one buy one
            for item in cart_items:
                item.subtotal = item.product.price * item.quantity
        else:
            cart_items = []

        user_session_key = request.session.session_key
        try:
            cart = Cart.objects.get(user_session_key=user_session_key)
            cart_quantity_total = sum(item.quantity for item in cart.cartitem_set.all())
        except Cart.DoesNotExist:
            cart_quantity_total = 0
        

        # Render the checkout page with the cart items for display
        return render(request, 'User/checkout.html', {'cart_items': cart_items, 'total_price' : total_price, 'sub_total_price' : sub_total_price, 'cart_quantity_total' : cart_quantity_total, })



def order_confirmation(request, order_id):
    # Get the order based on the provided order_id
    order = Order.objects.get(pk=order_id)

    # Render the order confirmation page with the order details
    return render(request, 'User/order_confirmation.html', {'order': order})

from django.shortcuts import redirect, get_object_or_404

def delete_cart_item(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id)
    item.delete()
    return redirect('cart_items_view')

def delete_all_cart_items(request):
    session_key = request.session.session_key
    cart = Cart.objects.filter(user_session_key=session_key).first()
    if cart:
        cart.cartitem_set.all().delete()
    return redirect('cart_items_view')


def about(request):
    user_session_key = request.session.session_key
    try:
        cart = Cart.objects.get(user_session_key=user_session_key)
        cart_quantity_total = sum(item.quantity for item in cart.cartitem_set.all())
    except Cart.DoesNotExist:
        cart_quantity_total = 0
    
    context = {
        'cart_quantity_total' : cart_quantity_total,
    }
    return render(request, 'User/about.html', context)

def contact(request):
    user_session_key = request.session.session_key
    try:
        cart = Cart.objects.get(user_session_key=user_session_key)
        cart_quantity_total = sum(item.quantity for item in cart.cartitem_set.all())
    except Cart.DoesNotExist:
        cart_quantity_total = 0
    
    context = {
        'cart_quantity_total' : cart_quantity_total,
    }
    return render(request, 'User/contact.html', context)

def shop(request):
    products = Product.objects.all()
    
    # Assuming you are using user sessions and the session key to identify the cart
    user_session_key = request.session.session_key
    try:
        cart = Cart.objects.get(user_session_key=user_session_key)
        cart_quantity_total = sum(item.quantity for item in cart.cartitem_set.all())
    except Cart.DoesNotExist:
        cart_quantity_total = 0
    
    return render(request, 'User/shop.html', {'products': products, 'cart_quantity_total': cart_quantity_total})



def add_to_cart_three(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Ensure that the user has a session key (create one if it doesn't exist)
    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key
    cart, created = Cart.objects.get_or_create(user_session_key=session_key)

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"Cart Added Succes fully")
    return redirect('shop')