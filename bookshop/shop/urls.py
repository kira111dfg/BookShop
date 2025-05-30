from django.contrib import admin
from django.urls import path,include

from . import views

urlpatterns = [
    path('',views.BookList.as_view(),name='booklist'),
    path('book/<slug:slug>/', views.BookDetail.as_view(), name='book'),
    path('genre/<slug:genre_slug>/', views.GenreView.as_view(), name='genre'),
    path('tag/<slug:tag_slug>/', views.TagView.as_view(), name='tag'),
    path('search/',views.SearchView.as_view(),name='book_search'),
]
