
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponseRedirect
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework_simplejwt import views as jwt_views
from gameLibrary import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gameLibrary.urls')),
    path('authentication/', include('authentication.urls')),
    path('myapi/', include('myapi.urls')),
    path('social-auth/', include('social_django.urls', namespace="social")),
]
