from django.shortcuts import render

from django.urls import reverse, reverse_lazy

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView,ListView,CreateView
from itertools import chain
from django.contrib.auth.models import User

from .models import Book

class BookList(ListView):
    model=Book
    template_name='shop/booklist.html'
