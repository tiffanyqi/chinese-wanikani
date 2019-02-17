from django.urls import path

from . import views

urlpatterns = [
    path('learn/', views.learn_view, name='learn'),
    path('review/', views.review_view, name='review'),

    path('review_characters_list', views.get_characters_to_review, name='review_characters_list'),
    path('update_reviewed_character', views.update_reviewed_character, name='update_reviewed_character'),
    path('learn_character_list', views.get_characters_to_learn, name='learn_character_list'),
    path('update_learned_character', views.update_learned_character, name='update_learned_character'),
]
