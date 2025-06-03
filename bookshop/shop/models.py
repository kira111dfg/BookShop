from django.db import models

from django.urls import reverse

from django.contrib.auth.models import User
from django.utils.text import slugify

import re

from users.models import Profile


def slugify_cyrillic(value):
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
        'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch',
        'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya'
    }
    value = value.lower()
    value = ''.join(translit_dict.get(c, c) for c in value)
    value = re.sub(r'[^a-z0-9]+', '-', value)
    return slugify(value)


class Book(models.Model):
    title=models.CharField(max_length=100)
    price=models.PositiveIntegerField()
    description=models.TextField(max_length=500)
    img=models.ImageField(upload_to="img/", default=None,
                              blank=True, null=True)
    slug=models.SlugField(unique=True,blank=True)
    genre=models.ForeignKey('Genre',on_delete=models.PROTECT)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    tag= models.ManyToManyField('Tag', blank=True)
    url=models.URLField(blank=True,null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify_cyrillic(self.title)
            slug = base_slug
            counter = 1
            while Book.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book', kwargs={'slug': self.slug})

class Genre(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField( unique=True, db_index=True,blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('genre', kwargs={'genre_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify_cyrillic(self.title)
            slug = base_slug
            counter = 1
            while Genre.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

class Tag(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField( unique=True, db_index=True,blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify_cyrillic(self.title)
            slug = base_slug
            counter = 1
            while Tag.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)