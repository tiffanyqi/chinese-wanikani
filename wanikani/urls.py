from django.contrib import admin
from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('registration/', include('wanikani.registration.urls')),

    path('', views.index, name='index'),
    path('character/<str:character>/', views.character, name='character'),
    path('session/', include('wanikani.session.urls')),

    # API
    path('user/', views.user, name='user'),
    path('characters/', views.characters, name='characters'),

    # React catch all
    re_path(r'^(?:.*)/?$', views.home, name='home'),
]
