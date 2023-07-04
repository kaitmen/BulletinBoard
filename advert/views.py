from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic.base import TemplateView

from .filters import *
from .forms import ReviewForm


def home(request):
    return redirect('advert:adverts')


class AdvertView(TemplateView):
    template_name = "advert/lists.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        adverts = AdvertFilter(self.request.GET, queryset=Advert.objects.all())
        paginator = Paginator(adverts.qs, 10)
        page = self.request.GET.get("page")
        try:
            show_adverts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            show_adverts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            show_adverts = paginator.page(paginator.num_pages)

        context["adverts"] = show_adverts
        context["form"] = adverts.form
        return context


class AdvertViewDetail(FormMixin, DetailView):
    model = Advert
    context_object_name = 'advert'
    template_name = "advert/detail.html"
    form_class = ReviewForm

    def get_success_url(self):
        return reverse('advert:advert-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(AdvertViewDetail, self).get_context_data(**kwargs)
        context['form'] = ReviewForm()
        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.advert = self.object
        form.save()
        return super(AdvertViewDetail, self).form_valid(form)


class ReviewView(TemplateView):
    template_name = "review/lists.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = ReviewFilter(self.request.GET, queryset=Review.objects.filter(author=self.request.user))
        paginator = Paginator(reviews.qs, 10)
        page = self.request.GET.get("page")
        try:
            show_reviews = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            show_reviews = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            show_reviews = paginator.page(paginator.num_pages)

        context["reviews"] = show_reviews
        context["form"] = reviews.form
        return context


class AdvertCreate(LoginRequiredMixin, CreateView):
    model = Advert
    fields = ['title', 'body', 'category']
    template_name = 'advert/create_form.html'

    def get_success_url(self):
        return reverse('advert:advert-detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AdvertUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Advert
    fields = ['title', 'body', 'category']
    template_name = 'advert/update_form.html'

    def get_success_url(self):
        return reverse('advert:advert-detail', kwargs={'pk': self.object.id})

    def test_func(self):
        self.object = self.get_object()
        return self.object.author == self.request.user


class AdvertDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Advert
    success_url = reverse_lazy('advert:adverts')
    template_name = "confirm_delete.html"
    raise_exception = True

    def test_func(self):
        self.object = self.get_object()
        return self.object.author == self.request.user


class ReviewCreate(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['body']
    template_name = 'review/create_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ReviewUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    fields = ['body']
    template_name = 'review/update_form.html'

    def get_success_url(self):
        return reverse('advert:advert-detail', kwargs={'pk': self.object.advert.id})

    def test_func(self):
        self.object = self.get_object()
        return self.object.author == self.request.user or self.object.arvert.author == self.request.user


class ReviewDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = "confirm_delete.html"
    raise_exception = True

    def get_success_url(self):
        return reverse('advert:advert-detail', kwargs={'pk': self.object.advert.id})

    def test_func(self):
        self.object = self.get_object()
        return self.object.author == self.request.user or self.advert.object.author == self.request.user


@login_required
def swap_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.advert.author != request.user:
        return HttpResponseForbidden(_("You don't have access to this action"))
    else:
        review.active = not review.active
        review.save()
    return redirect('settings:settings')