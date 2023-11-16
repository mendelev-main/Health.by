from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class News(models.Model):
    title = models.CharField(max_length=200)
    body = RichTextField()
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField("Tag", blank=True, related_name="news")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news:detail", kwargs={"pk": self.pk})

    @property
    def rating(self) -> int:
        return self.upvote - self.downvote

    @property
    def upvote(self):
        return len(self.vote_set.filter(up=True))

    @property
    def downvote(self):
        return len(self.vote_set.filter(up=False))


class Vote(models.Model):
    post = models.ForeignKey(to=News, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    up = models.BooleanField(null=False)

    class Meta:
        unique_together = ("post", "user")


class Tag(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title
