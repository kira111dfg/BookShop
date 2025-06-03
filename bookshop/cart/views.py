from django.shortcuts import get_object_or_404, redirect
from .models import CartItem
from shop.models import Book
from django.shortcuts import render


from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, book=book)

    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_view')


@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    paginator = Paginator(cart_items, 2)  

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'cart/cart_view.html', {
        'page_obj': page_obj,
        'cart_items': page_obj.object_list,
    })


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('cart_view')





@login_required
def increase_quantity(request, book_id):
    cart_item = get_object_or_404(CartItem, user=request.user, book_id=book_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_view')  # или твой url name для корзины

@login_required
def decrease_quantity(request, book_id):
    cart_item = get_object_or_404(CartItem, user=request.user, book_id=book_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        # если количество 1 и нажали уменьшить — можно удалить из корзины
        cart_item.delete()
    return redirect('cart_view')
