from django.contrib import admin
from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', include('wanikani.registration.urls')),
    path('session/', include('wanikani.session.urls')),

    # API
    path('user/', views.user, name='user'),

    # React catch all
    path('home/', views.home, name='home'),
    re_path(r'^(?:.*)/?$', views.home, name='home'),
]
