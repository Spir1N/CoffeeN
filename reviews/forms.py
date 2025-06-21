# apps/catalog/forms.py
from django import forms
from .models import Review, Question

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, "★" * i) for i in range(1, 6)]

    rating = forms.TypedChoiceField(
        coerce=int,
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
        error_messages={"required": "Поставьте оценку от 1 до 5"}
    )

    class Meta:
        model = Review
        fields = ("rating", "body")
        widgets = {
            "body": forms.Textarea(attrs={"rows": 3, "placeholder": "Ваш отзыв"}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ("body",)
        widgets = {
            "body": forms.Textarea(attrs={"rows": 3, "placeholder": "Задайте вопрос"}),
        }
