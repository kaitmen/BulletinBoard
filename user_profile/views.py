from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models.functions import Now
from django.template.response import TemplateResponse

from django.shortcuts import render, redirect
from django.utils.translation import gettext as _

from django.contrib import messages

from . filters import *
from .forms import *
from .models import *


@login_required
def settings(request):
    owm_reviews = OwnReviewFilter(request.GET, queryset=Review.objects.filter(author=request.user))
    other_reviews = OthersReviewFilter(request.GET, queryset=Review.objects.filter(advert__author=request.user))

    own_paginator = Paginator(owm_reviews.qs, 10)
    others_paginator = Paginator(other_reviews.qs, 10)
    page = request.GET.get("page")

    try:
        show_own = own_paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        show_own = own_paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        show_own = own_paginator.page(own_paginator.num_pages)

    try:
        show_others = others_paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        show_others = others_paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        show_others = others_paginator.page(others_paginator.num_pages)

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    ctx = {
        'user_form': user_form,
        "profile_form": profile_form,
        "own_reviews": show_own,
        "own_filter": owm_reviews.form,
        "others_reviews": show_others,
        "others_filter": other_reviews.form,
    }
    return render(request, 'settings/profile.html', ctx)


def register_code(request, token):
    db_code = RegisterCode.objects.filter(token=token, expires_at__gt=Now()).get()

    if not db_code:
        return HttpResponseNotFound(_("Link is no longer valid"))

    if request.method == 'POST':
        enter_code = request.POST.get("code")
        if enter_code == db_code.code:
            return redirect('login')

    return TemplateResponse(request, "registration/code.html", {"user": db_code.user})


def signup(request):
    """Register a new user."""
    if request.method == 'POST':
        form = ExtendUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return TemplateResponse(request, 'registration/signup_success.html')
    else:
        form = ExtendUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})