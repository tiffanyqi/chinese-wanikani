from django.urls import path

from . import views

urlpatterns = [
    # user pathways
    path('learn/', views.learn_view, name='learn'),
    path('review/', views.review_view, name='review'),
    # path('summary/', views.summary_view, name='summary'),

    # api pathways
    path('characters/', views.characters),
    path('characters/learn/', views.characters_to_learn),
    path('characters/learn/update/', views.update_learned_character),
    path('characters/review/', views.characters_to_review),
    path('characters/review/update/', views.update_reviewed_character),
    path('characters/level/', views.characters_at_level),
    path('characters/<str:character>/', views.character),
]
