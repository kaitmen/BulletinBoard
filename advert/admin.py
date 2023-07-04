from django.contrib import admin

from .models import *


class AdvertAdmin(admin.ModelAdmin):
    fields = ['author', 'title', 'body', 'category']


class ReviewAdmin(admin.ModelAdmin):
    fields = ['author', 'advert', 'body', 'active']


admin.site.register(Advert, AdvertAdmin)
admin.site.register(Review, ReviewAdmin)
