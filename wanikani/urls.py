from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('characters/', views.characters, name='characters'),
    path('character/<str:character>/', views.character, name='character'),
    path('user/', views.get_user, name='user'),
    path('test/', views.test, name='test'),

    path('registration/', include('wanikani.registration.urls')),
    path('session/', include('wanikani.session.urls')),
]
