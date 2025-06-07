from django.urls import reverse
import stripe
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
from shop.models import Order, OrderItem,Book

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def create_checkout_session(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect('cart')  # или показать ошибку

    # Создаем заказ, но не помечаем как оплаченный
    order = Order.objects.create(user=request.user)

    line_items = []
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            book=item.book,
            quantity=item.quantity,
            price=item.book.price
        )

        line_items.append({
            'price_data': {
                'currency': 'usd',
                'unit_amount': item.book.price * 100,
                'product_data': {'name': item.book.title},
            },
            'quantity': item.quantity,
        })


    success_url = request.build_absolute_uri('/payment/success/?session_id={CHECKOUT_SESSION_ID}')

    cancel_url = request.build_absolute_uri(reverse('payment_cancel'))
    
    session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=line_items,
    mode='payment',
    success_url=request.build_absolute_uri(
        reverse('payment_success')
    ) + '?session_id={CHECKOUT_SESSION_ID}',
    cancel_url=request.build_absolute_uri(reverse('payment_cancel')),
    client_reference_id=str(order.id),
)


    print("Success URL:", request.build_absolute_uri('/payment/success/?session_id={CHECKOUT_SESSION_ID}'))
    return redirect(session.url, code=303)

@login_required
def create_checkout_session_for_book(request, book_id):
    from django.shortcuts import get_object_or_404

    book = get_object_or_404(Book, id=book_id)

    # Создаем временный заказ с одной книгой
    order = Order.objects.create(user=request.user, address='временно')

    OrderItem.objects.create(
        order=order,
        book=book,
        quantity=1,
        price=book.price
    )

    line_items = [{
        'price_data': {
            'currency': 'usd',
            'unit_amount': book.price * 100,
            'product_data': {'name': book.title},
        },
        'quantity': 1,
    }]

    success_url = request.build_absolute_uri(reverse('payment_success'))
    cancel_url = request.build_absolute_uri(reverse('payment_cancel'))

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
        client_reference_id=str(order.id),
    )

    return redirect(session.url, code=303)

from django.http import HttpResponse
import stripe

@login_required
def payment_success(request):
    session_id = request.GET.get("session_id")
    if not session_id:
        return HttpResponse("Session ID отсутствует", status=400)

    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except stripe.error.InvalidRequestError:
        return HttpResponse("❌ Ошибка при получении Stripe-сессии", status=400)

    if session.payment_status == "paid":
        order_id = session.client_reference_id
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            if not order.paid:
                order.paid = True
                # Пример: заполняем адрес, если передан
                address = session.get("customer_details", {}).get("address", {})
                order.address = address.get("line1", "Без адреса")
                order.save()

                # Очистить корзину
                CartItem.objects.filter(user=request.user).delete()

        except Order.DoesNotExist:
            return HttpResponse("Заказ не найден", status=404)

        return render(request, 'payment/success.html')
    else:
        return HttpResponse("❌ Оплата не прошла", status=400)


@login_required
def payment_cancel(request):
    return render(request, 'payment/cancel.html')