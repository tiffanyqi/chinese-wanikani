from datetime import datetime

from django.test import TestCase

from wanikani.models import BaseCharacter, ProgressCharacter, User
from wanikani.session.util import get_level, get_upcoming_review_date

class SessionLevelTestCase(TestCase):

  def setup(self):
    self.user = User(
      email='email',
      level=1,
      username='username',
    )
    self.base = BaseCharacter(
      character='没',
      definitions=['definition'],
      pinyin=['pinyin'],
      user_level=1,
    )
    self.character = ProgressCharacter(
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
    )

  def test_level_increments_correctly(self):
    self.setup()
    self.assertEqual(get_level(self.character), 2)

  def test_level_decrements_correctly(self):
    self.setup()
    self.character.num_current_incorrect = {
      'pinyin': 1,
      'definitions': 0,
    }
    self.assertEqual(get_level(self.character), 1)


class SessionReviewDateTestCase(TestCase):
  now = datetime(2019, 1, 27, 10, 55)

  def test_upcoming_review_date_increments_and_rounds_correctly(self):    
    self.assertEqual(get_upcoming_review_date(self.now, 1), datetime(2019, 1, 27, 12, 00))
    self.assertEqual(get_upcoming_review_date(self.now, 2), datetime(2019, 1, 27, 14, 00))
    self.assertEqual(get_upcoming_review_date(self.now, 5), datetime(2019, 1, 28, 18, 00))
