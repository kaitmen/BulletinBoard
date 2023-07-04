import django_filters
from django.forms import DateInput, NumberInput

from .models import *


class AdvertFilter(django_filters.FilterSet):
    created_at__gt = django_filters.DateFilter(field_name='created_at', lookup_expr='startswith',
                                               widget=DateInput(attrs={'type': 'date', 'placeholder': 'Date start'}))
    created_at__lt = django_filters.DateFilter(field_name='created_at', lookup_expr='endswith',
                                               widget=DateInput(attrs={'type': 'date', 'placeholder': 'Date end'}))

    class Meta:
        model = Advert
        fields = ['author', 'title', 'category']


class ReviewFilter(django_filters.FilterSet):
    created_at__gt = django_filters.DateFilter(field_name='created_at', lookup_expr='startswith',
                                               widget=DateInput(attrs={'type': 'date', 'placeholder': 'Date start'}))
    created_at__lt = django_filters.DateFilter(field_name='created_at', lookup_expr='endswith',
                                               widget=DateInput(attrs={'type': 'date', 'placeholder': 'Date end'}))

    class Meta:
        model = Review
        fields = ['advert', 'active']