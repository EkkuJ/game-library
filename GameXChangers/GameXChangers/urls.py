
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponseRedirect
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework_simplejwt import views as jwt_views
from gameLibrary import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gameLibrary.urls')),
    path('authentication/', include('authentication.urls')),
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
