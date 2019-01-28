from django.urls import path

from . import views

urlpatterns = [
    path('current_level_characters_list', views.get_user_level_characters, name='current_level_characters_list'),
    path('post_updated_character', views.post_updated_character, name='post_updated_character'),
]
