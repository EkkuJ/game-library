
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponseRedirect
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gameLibrary.urls')),
    path('authentication/', include('authentication.urls'))
]