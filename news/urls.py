from django.urls import path

from . import views


app_name = "news"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("create/", views.NewsCreateView.as_view(), name="create_news"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/upvote", views.upvote, name="upvote"),
    path("<int:pk>/downvote", views.downvote, name="downvote"),
    path("create_tag/", views.TagCreateView.as_view(), name="create_tag"),
    path("index_tag/", views.IndexTagView.as_view(), name="index_tag"),
    path("detail_tag/<int:pk>/", views.DetailTagView.as_view(), name="detail_tag"),
]
