from django import shortcuts
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views import generic

from .models import News, Tag, Vote


class IndexView(generic.ListView):
    template_name = "news/index.html"
    context_object_name = "news"

    def get_queryset(self):
        return News.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")


class DetailView(generic.DetailView):
    model = News
    template_name = "news/detail.html"


class NewsCreateView(LoginRequiredMixin, generic.CreateView):
    model = News
    fields = [
        "title",
        "body",
        "tag",
    ]
    template_name = "news/create_news.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def upvote(request, pk: int):
    return _vote(request=request, pk=pk, up=True)


def downvote(request, pk: int):
    return _vote(request=request, pk=pk, up=False)


def _vote(request, pk: int, up: bool):
    post = shortcuts.get_object_or_404(News, pk=pk)
    Vote.objects.update_or_create(post=post, user=request.user, defaults={"up": up})
    return shortcuts.redirect("news:detail", pk=pk)


class TagCreateView(LoginRequiredMixin, generic.CreateView):
    model = Tag
    fields = [
        "title",
    ]
    template_name = "news/create_tag.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class IndexTagView(generic.ListView):
    template_name = "news/index_tag.html"
    context_object_name = "tags"

    def get_queryset(self):
        tags = Tag.objects.all()
        sorted_tags = sorted(tags, key=lambda tag: tag.title)
        return sorted_tags


class DetailTagView(generic.DetailView):
    model = Tag
    template_name = "news/detail_tag.html"
