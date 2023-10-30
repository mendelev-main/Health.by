from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('user_profile/', include("user_profile.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns.extend(
#         [
#             static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
#         ]
#     )
