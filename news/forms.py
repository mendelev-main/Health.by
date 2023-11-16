from django import forms

from .models import News, Tag


class PostForm(forms.ModelForm):
    class Meta:
        model = News
        fields = [
            "title",
            "body",
            "tag",
        ]


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = [
            "title",
        ]
