from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView
from .models import Product, Review, Question
from .forms import ReviewForm, QuestionForm
from django.http import Http404


class ProductDetailView(DetailView):
    model = Product
    template_name = "reviews/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        user_review = None
        if self.request.user.is_authenticated:
            user_review = self.object.reviews.filter(author=self.request.user).first()

        ctx |= {
            "user_review": user_review,          # отзыв текущего пользователя или None
            "review_form": ReviewForm() if user_review is None else None,
            "question_form": QuestionForm(),
        }
        return ctx


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm

    def form_valid(self, form):
        form.instance.author  = self.request.user
        form.instance.product = Product.objects.get(pk=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.product.get_absolute_url() + "#reviews"


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return self.get_object().product.get_absolute_url() + "#reviews"


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm

    def form_valid(self, form):
        form.instance.author  = self.request.user
        form.instance.product = Product.objects.get(pk=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.product.get_absolute_url() + "#questions"


class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return self.get_object().product.get_absolute_url() + "#questions"


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Единственный отзыв автора → правка.
    URL получают pk самого отзыва.
    """
    model = Review
    form_class = ReviewForm
    template_name = "reviews/review_form.html"     # можно переиспользовать шаблон create

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return self.object.product.get_absolute_url() + "#reviews"

    # дополнительная защита: если кто‑то полезет редактировать чужой отзыв
    def handle_no_permission(self):
        raise Http404
