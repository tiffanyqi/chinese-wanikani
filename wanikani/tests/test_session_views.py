from datetime import datetime

from django.test import TestCase

from wanikani.session.views import update_character
from wanikani.tests.util import (
  create_test_base_character,
  create_test_progress_character,
  create_test_user,
)

class SessionUpdateReviewedCharacterTestCase(TestCase):

  def setup(self):
    self.user = create_test_user()
    self.base = create_test_base_character('没')
    self.character = create_test_progress_character(self.base, self.user)

  def create_updated_character(self, data):
    return update_character(
      data['both_correct'],
      data['character'],
      data['is_complete'],
      data['is_correct'],
      data['type'],
      data['user'],
    )

  def test_updates_character_correctly_if_answered_correctly(self):
    self.setup()
    data = {
      'both_correct': False,
      'character': '没',
      'is_complete': False,
      'is_correct': True,
      'type': 'pinyin',
      'user': self.user,
    }
    character = self.create_updated_character(data)
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
      'user': self.user,
    }
    character = self.create_updated_character(data)
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
      'both_correct': False,
      'character': '没',
      'is_complete': False,
      'is_correct': False,
      'type': 'pinyin',
      'user': self.user,
    }
    character = self.create_updated_character(data)
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
      'user': self.user,
    }
    character = self.create_updated_character(data)
    self.assertEquals(character.get('num_times_shown'), 0)
    self.assertEquals(character.get('num_correct').get('pinyin'), 1)
    self.assertEquals(character.get('num_correct').get('definitions'), 0)
    self.assertEquals(character.get('num_correct').get('all'), 0)
    self.assertIsNotNone(character.get('unlocked_date'))
    self.assertEquals(character.get('level'), 1)
    self.assertEquals(character.get('num_current_incorrect').get('pinyin'), 1)
    self.assertIsNone(character.get('upcoming_review_date'))
