from django.urls import path

from . import views


app_name = "user_profile"
urlpatterns = [
    path("create/", views.ProfileCreateView.as_view(), name="create_profile"),
    path("<int:pk>/", views.ProfileDetailView.as_view(), name="detail_profile"),
]
