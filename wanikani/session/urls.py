from django.urls import path

from . import views

urlpatterns = [
    path('characters/', views.characters),
    path('characters/learn/', views.characters_to_learn),
    path('characters/learn/update/', views.update_learned_character),
    path('characters/review/', views.characters_to_review),
    path('characters/review/update/', views.update_reviewed_character),
    path('characters/incorrect/', views.last_session_characters_incorrect),
    path('characters/correct/', views.last_session_characters_correct),
    path('characters/level/', views.characters_at_level),
    path('characters/<str:character>/', views.character),
]
