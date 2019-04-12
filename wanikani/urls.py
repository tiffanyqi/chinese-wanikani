from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),

    path('', views.index, name='index'),
    path('characters/', views.characters, name='characters'),
    path('character/<str:character>/', views.character, name='character'),
    path('user/', views.get_user, name='user'),

    path('registration/', include('wanikani.registration.urls')),
    path('session/', include('wanikani.session.urls')),
]
