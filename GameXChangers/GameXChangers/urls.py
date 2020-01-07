
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gameLibrary/', include('gameLibrary.urls')),
    path('authentication/', include('authentication.urls'))
]
