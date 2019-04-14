from django.contrib import admin
from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', include('wanikani.registration.urls')),
    path('session/', include('wanikani.session.urls')),

    # API
    path('user/', views.user, name='user'),
    path('request_characters/', views.characters, name='characters'),
    path('request_characters/learn/', views.characters_to_learn, name='characters_to_learn'),
    path('request_characters/review/', views.characters_to_review, name='characters_to_review'),
    path('request_characters/level/', views.characters_at_level, name='characters_at_level'),
    path('request_characters/<str:character>/', views.character, name='character'),

    # React catch all
    path('home/', views.home, name='home'),
    re_path(r'^(?:.*)/?$', views.home, name='home'),
]
