from django.db import models
from django.contrib.auth.models import User
from shop.models import Book  # если у тебя книга в другом приложении

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.book.title} ({self.quantity})"

    def total_price(self):
        return self.book.price * self.quantity  # если у книги есть price
