from datetime import datetime

from django.test import TestCase

from wanikani.models import BaseCharacter, ProgressCharacter, User
from wanikani.session.views import update_character

class SessionUpdateCharacterTestCase(TestCase):

  def setup(self):
    self.user = User.objects.create(
      email='email',
      level=1,
      username='username',
    )
    self.base = BaseCharacter.objects.create(
      character='没',
      definitions=['definition'],
      pinyin=['pinyin'],
      user_level=1,
    )
    self.character = ProgressCharacter.objects.create(
      character=self.base,
      user=self.user,
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
      level=1,
      unlocked_date=datetime.now()
    )

  def test_updates_character_correctly_if_answered_correctly(self):
    self.setup()
    data = {
      'character': '没',
      'is_complete': False,
      'is_correct': True,
      'type': 'pinyin',
    }
    character = update_character(self.user, data)
    self.assertEquals(character.get('num_times_shown'), 0)
    self.assertEquals(character.get('num_correct').get('pinyin'), 1)
    self.assertEquals(character.get('num_correct').get('definitions'), 0)
    self.assertEquals(character.get('num_correct').get('all'), 0)
    self.assertIsNotNone(character.get('unlocked_date'))
    self.assertEquals(character.get('level'), 1)
    self.assertEquals(character.get('num_current_incorrect').get('pinyin'), 0)
    self.assertIsNone(character.get('upcoming_review_date'))

    data = {
      'both_correct': True,
      'character': '没',
      'is_complete': True,
      'is_correct': True,
      'type': 'definitions',
    }
    character = update_character(self.user, data)
    self.assertEquals(character.get('num_times_shown'), 1)
    self.assertEquals(character.get('num_correct').get('pinyin'), 1)
    self.assertEquals(character.get('num_correct').get('definitions'), 1)
    self.assertEquals(character.get('num_correct').get('all'), 1)
    self.assertIsNotNone(character.get('unlocked_date'))
    self.assertEquals(character.get('level'), 2)
    self.assertEquals(character.get('num_current_incorrect').get('pinyin'), 0)
    self.assertIsNotNone(character.get('upcoming_review_date'))

  def test_updates_character_correctly_if_answered_incorrectly(self):
    self.setup()
    data = {
      'character': '没',
      'is_complete': False,
      'is_correct': False,
      'type': 'pinyin',
    }
    character = update_character(self.user, data)
    self.assertEquals(character.get('num_times_shown'), 0)
    self.assertEquals(character.get('num_correct').get('pinyin'), 0)
    self.assertEquals(character.get('num_correct').get('definitions'), 0)
    self.assertEquals(character.get('num_correct').get('all'), 0)
    self.assertIsNotNone(character.get('unlocked_date'))
    self.assertEquals(character.get('level'), 1)
    self.assertEquals(character.get('num_current_incorrect').get('pinyin'), 1)
    self.assertIsNone(character.get('upcoming_review_date'))

    data = {
      'both_correct': False,
      'character': '没',
      'is_complete': False,
      'is_correct': True,
      'type': 'pinyin',
    }
    character = update_character(self.user, data)
    self.assertEquals(character.get('num_times_shown'), 0)
    self.assertEquals(character.get('num_correct').get('pinyin'), 1)
    self.assertEquals(character.get('num_correct').get('definitions'), 0)
    self.assertEquals(character.get('num_correct').get('all'), 0)
    self.assertIsNotNone(character.get('unlocked_date'))
    self.assertEquals(character.get('level'), 1)
    self.assertEquals(character.get('num_current_incorrect').get('pinyin'), 1)
    self.assertIsNone(character.get('upcoming_review_date'))
