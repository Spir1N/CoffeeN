# apps/catalog/urls.py
from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("products/<int:pk>/", views.ProductDetailView.as_view(), name="product"),
    path("products/<int:pk>/review/", views.ReviewCreateView.as_view(),  name="review_add"),
    path("reviews/<int:pk>/delete/", views.ReviewDeleteView.as_view(),  name="review_del"),
    path("products/<int:pk>/question/", views.QuestionCreateView.as_view(), name="question_add"),
    path("questions/<int:pk>/delete/", views.QuestionDeleteView.as_view(), name="question_del"),
    path("<int:pk>/edit/", views.ReviewUpdateView.as_view(), name="review_edit"),
]
