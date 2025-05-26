from django.db import models

from django.urls import reverse

from django.contrib.auth.models import User
from django.utils.text import slugify

class Book(models.Model):
    title=models.CharField(max_length=100)
    price=models.PositiveIntegerField()
    description=models.TextField(max_length=500)
    img=models.ImageField(upload_to="img/", default=None,
                              blank=True, null=True)
    slug=models.SlugField(unique=True)
    genre=models.ForeignKey('Genre',on_delete=models.PROTECT)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
    tags= models.ManyToManyField('Tag', blank=True)
    url=models.URLField(blank=True,null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book', kwargs={'book_slug': self.slug})

class Genre(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('genre', kwargs={'genre_slug': self.slug})

class Tag(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})