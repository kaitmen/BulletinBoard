from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import pgettext_lazy
from tinymce import models as tinymce_models

from . import CategoryName


class Advert(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=pgettext_lazy('Advert model', 'Author'))
    title = models.CharField(max_length=220, verbose_name=pgettext_lazy('Advert model', 'Title'))
    body = tinymce_models.HTMLField()
    category = models.CharField(max_length=128, choices=CategoryName.CHOICES,
                                verbose_name=pgettext_lazy('Advert model', 'Category'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=pgettext_lazy('Advert model', 'Created Date'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=pgettext_lazy('Advert model', 'Updated Date'))

    def __str__(self):
        return self.title

    def get_reviews_count(self):
        return self.reviews.filter(active=True).count()

    def get_reviews(self):
        return self.reviews.all()

    def get_active_reviews(self):
        return self.reviews.filter(active=True)


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=pgettext_lazy('Review model', 'Author'))
    advert = models.ForeignKey(Advert, related_name='reviews', on_delete=models.CASCADE,
                               verbose_name=pgettext_lazy('Review model', 'Advert'))
    body = tinymce_models.HTMLField()
    active = models.BooleanField(default=False, verbose_name=pgettext_lazy('Review model', 'Active'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=pgettext_lazy('Review model', 'Created Date'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=pgettext_lazy('Review model', 'Updated Date'))

    def __str__(self):
        return f"{self.author.username} - {self.advert.title}"
