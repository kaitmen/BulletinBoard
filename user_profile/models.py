from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import pgettext_lazy

from datetime import timedelta
from django.utils import timezone


def in_three_days():
    return timezone.now() + timedelta(days=3)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=pgettext_lazy('Profile model', 'User'))
    active = models.BooleanField(default=False, verbose_name=pgettext_lazy('Profile model', 'Active'))
    get_newsletter = models.BooleanField(default=False, verbose_name=pgettext_lazy('Profile model', 'Get Newsletter'))

    def get_own_reviews_count(self):
        return self.user.review_set.count()

    def get_others_reviews_count(self):
        count = 0
        for advert in self.user.advert_set.all():
            count += advert.reviews.count()
        return count

    def get_own_reviews(self):
        return self.user.review_set.all()

    def get_others_reviews(self):
        reviews = []
        for advert in self.user.advert_set.all():
            reviews.extend(advert.reviews.all())
        return reviews


class RegisterCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=pgettext_lazy('RegisterCode model', 'User'))
    code = models.CharField(max_length=220, verbose_name=pgettext_lazy('RegisterCode model', 'Code'))
    token = models.TextField(verbose_name=pgettext_lazy('RegisterCode model', 'Token'))
    registered = models.BooleanField(default=False, verbose_name=pgettext_lazy('RegisterCode model', 'Registered'))
    expires_at = models.DateTimeField(default=in_three_days, verbose_name=pgettext_lazy('RegisterCode model', 'Expires At'))