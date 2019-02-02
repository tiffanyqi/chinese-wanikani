from datetime import datetime

from django.test import TestCase

from wanikani.session.util import check_level_up, get_level, get_upcoming_review_date
from wanikani.tests.util import (
  create_test_base_character,
  create_test_progress_character,
  create_test_user,
)

class SessionLevelTestCase(TestCase):

  def setup(self):
    self.user = create_test_user()
    self.base = create_test_base_character('没')
    self.character = create_test_progress_character(self.base, self.user)

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


class SessionUpdateUserLevelTestCase(TestCase):

  def setup(self):
    self.user = create_test_user()
    self.base1 = create_test_base_character('没')
    self.base2 = create_test_base_character('时')
    self.base3 = create_test_base_character('有')

  def test_successful_level_up(self):
    self.setup()
    create_test_progress_character(self.base1, self.user, level=5)
    create_test_progress_character(self.base2, self.user, level=5)
    create_test_progress_character(self.base3, self.user, level=5)
    self.assertEqual(check_level_up(self.user), True)

  def test_unsuccessful_level_up(self):
    self.setup()
    create_test_progress_character(self.base1, self.user, level=4)
    create_test_progress_character(self.base2, self.user, level=5)
    create_test_progress_character(self.base3, self.user, level=5)
    self.assertEqual(check_level_up(self.user), False)

  def test_successful_level_up_different_user(self):
    self.setup()
    separate_user = create_test_user(email='hi', username='hi')
    create_test_progress_character(self.base1, separate_user, level=4)
    create_test_progress_character(self.base2, self.user, level=5)
    create_test_progress_character(self.base3, self.user, level=5)
    self.assertEqual(check_level_up(self.user), True)
