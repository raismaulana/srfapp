from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('sadmin/', admin.site.urls),
    path('petugas/', include('petugas.urls')),
    path('', include('blog.urls')),
]
