# payment/urls.py
from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('payment/create_session/book/<int:book_id>/', views.create_checkout_session_for_book, name='create_checkout_session_for_book'),
    path('payment/create_session/cart/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.payment_success, name='payment_success'),
    path('cancel/',views.payment_cancel, name='payment_cancel'),
]
