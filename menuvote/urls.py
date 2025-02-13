from django.contrib import admin
from django.urls import path, include

#Main url's of application
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('restaurants/', include('restaurants.urls')),
    path('voting/', include('voting.urls')),
]
