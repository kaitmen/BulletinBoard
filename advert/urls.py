from django.urls import path

from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('adverts', AdvertView.as_view(), name='adverts'),
    path('reviews', ReviewView.as_view(), name='reviews'),

    path('adverts/add', AdvertCreate.as_view(), name='advert-add'),
    path('adverts/<int:pk>', AdvertViewDetail.as_view(), name='advert-detail'),
    path('adverts/<int:pk>/update', AdvertUpdate.as_view(), name='advert-update'),
    path('adverts/<int:pk>/delete', AdvertDelete.as_view(), name='advert-delete'),

    path('reviews/add', ReviewCreate.as_view(), name='review-add'),
    path('reviews/<int:pk>/detail/', ReviewUpdate.as_view(), name='review-detail'),
    path('reviews/<int:pk>/update', ReviewUpdate.as_view(), name='review-update'),
    path('reviews/<int:pk>/delete', ReviewDelete.as_view(), name='review-delete'),

    path('reviews/swap_review/<int:pk>', swap_review, name='swap-review'),
]