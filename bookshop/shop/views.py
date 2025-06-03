from django.shortcuts import render

from django.urls import reverse, reverse_lazy

from django.db.models import Q


from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView,ListView,CreateView
from itertools import chain
from django.contrib.auth.models import User

from .models import Book, Genre, Tag

class BookList(ListView):
    model=Book
    template_name='shop/booklist.html'
    context_object_name='books'

class BookDetail(DetailView):
    model=Book
    template_name='shop/bookdetail.html'
    context_object_name='book'


class GenreView(ListView):
    model = Book
    template_name = 'shop/genre.html'
    context_object_name = 'genre'
    genre=None

    def get_queryset(self):
        self.genre = Genre.objects.get(slug=self.kwargs['genre_slug'])
        queryset = Book.objects.all().filter(genre__slug=self.genre.slug)
        return queryset



class TagView(ListView):
    model = Book
    template_name = 'shop/tag.html'
    context_object_name = 'tag'
    tag=None

    def get_queryset(self):
        self.tag = Tag.objects.get(slug=self.kwargs['tag_slug'])
        queryset = Book.objects.all().filter(tag__slug=self.tag.slug)
        return queryset





class SearchView(ListView):
    model = Book
    template_name = 'shop/book_search.html'
    context_object_name = 'books'

    def get_queryset(self):
        queryset = Book.objects.all()
        title = self.request.GET.get('title', '').strip()
        genre = self.request.GET.get('genre', '').strip()

        if title and genre:
            queryset = queryset.filter(
                Q(title__icontains=title) &
                Q(genre__title__icontains=genre)
            )
        elif title:
            queryset = queryset.filter(title__icontains=title)
        elif genre:
            queryset = queryset.filter(genre__title__icontains=genre)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.request.GET.get('title', '')
        context['genre'] = self.request.GET.get('genre', '')
        return context
