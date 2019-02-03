from datetime import datetime

from wanikani.models import BaseCharacter, ProgressCharacter, User

def create_test_user(email='email', level=1, username='username'):
  return User.objects.create(
      email=email,
      level=level,
      username=username,
    )

def create_test_base_character(character, user_level=1):
  return BaseCharacter.objects.create(
      character=character,
      definitions=['definition'],
      pinyin=['pinyin'],
      user_level=user_level,
    )

def create_test_progress_character(base_object, user_object, level=1, unlocked_date=datetime.now()):
  return ProgressCharacter.objects.create(
      character=base_object,
      user=user_object,
      num_correct={
        'pinyin': 0,
        'definitions': 0,
        'all': 0
      },
      num_current_incorrect={
        'pinyin': 0,
        'definitions': 0,
      },
      num_times_shown=0,
      level=level,
      unlocked_date=unlocked_date,
    )
