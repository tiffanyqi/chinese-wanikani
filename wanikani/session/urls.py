from django.urls import path

from . import views

urlpatterns = [
    path('learn/', views.learn_view, name='learn'),
    path('review/', views.review_view, name='review'),

    path('current_level_characters_list', views.get_characters_to_review, name='current_level_characters_list'),
    path('post_updated_character', views.post_updated_character, name='post_updated_character'),
]
