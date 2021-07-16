from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("monk.urls")),
    path('webhook/', include("monk.urls")),
    path('orgdebug/', include("monk.urls")),
]
