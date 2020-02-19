
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gameLibrary.urls')),
    path('authentication/', include('authentication.urls')),
    path('social-auth/', include('social_django.urls', namespace="social"))
]