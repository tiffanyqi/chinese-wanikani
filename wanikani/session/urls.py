from django.urls import path

from . import views

urlpatterns = [
    path('characters_list/', views.test_characters, name='test_characters'),
]
