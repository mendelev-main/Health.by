from django.urls import path

from . import views


app_name = "user_profile"
urlpatterns = [
    path('search_doctor/', views.SearchDoctorView.as_view(), name='search_doctor'),
    path('search/', views.SearchView.as_view(), name='index'),
    path("create/", views.ProfileCreateView.as_view(), name="create_profile"),
    path(
        "create_doctor/",
        views.ProfileDoctorCreateView.as_view(),
        name="create_profile_doctor",
    ),
    path("<int:pk>/", views.ProfileDetailView.as_view(), name="detail_profile"),
    path(
        "doctor/<int:pk>/",
        views.ProfileDoctorDetailView.as_view(),
        name="detail_profile_doctor",
    ),
    path(
        "<int:pk>/create_treatment/",
        views.TreatmentCreateView.as_view(),
        name="create_treatment",
    ),
    path(
        "treatment/<int:pk>",
        views.TreatmentDetailView.as_view(),
        name="detail_treatment",
    ),
]
