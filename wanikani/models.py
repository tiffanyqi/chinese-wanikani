from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone


class User(AbstractBaseUser):
    name = models.CharField(null=True, max_length=50)
    email = models.CharField(null=True, max_length=50)
    level = models.CharField(default=1, max_length=50)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    username = models.CharField(null=True, max_length=50)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_session = models.IntegerField(default=0)


# Currently not being used
class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_started = models.DateTimeField(default=timezone.now)
    session_type = models.CharField(null=True, max_length=50) # review or lesson
    num_correct_pinyin = models.IntegerField(default=0)
    num_correct_definitions = models.IntegerField(default=0)
    num_correct_all = models.IntegerField(default=0)
    total_items = models.IntegerField(default=0)
    complete = models.BooleanField(default=False)
    characters = JSONField() # {character: {meaning: 1, pinyin: 0}}


class BaseCharacter(models.Model):
    """
    Character that contains information about the character, such as
    definitions and pinyin.
    """
    character = models.CharField(null=True, max_length=50)
    definitions = JSONField()
    pinyin = JSONField()
    hsk_level = models.IntegerField(default=0)
    frequency = models.IntegerField(default=0)
    user_level = models.IntegerField(default=0)

    def to_json(self):
        keys = ['character', 'definitions', 'pinyin', 'user_level']
        return {key: getattr(self, key) for key in keys}


class ProgressCharacter(models.Model):
    """
    Character that contains information about the character in relation
    to the user's progress, such as the number of correct responses and
    the latest session date.
    """
    character = models.ForeignKey(BaseCharacter, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num_correct = JSONField() # {pinyin: int, definitions: int, all: int}
    num_current_incorrect = JSONField() # {pinyin: int, definitions: int}
    num_times_shown = models.IntegerField(default=0)
    unlocked_date = models.DateTimeField(default=None, null=False)
    upcoming_review_date = models.DateTimeField(default=None, null=True)
    last_reviewed_date = models.DateTimeField(default=None, null=True)
    level = models.IntegerField(default=1, null=False)
    last_session = models.IntegerField(default=0)

    def to_json(self):
        character_keys = ['character', 'definitions', 'pinyin', 'user_level']
        keys = ['num_correct',
                'num_current_incorrect',
                'num_times_shown',
                'unlocked_date',
                'upcoming_review_date',
                'last_reviewed_date',
                'level']
        attributes = {key: getattr(self, key) for key in keys}
        for key in character_keys:
            attributes[key] = getattr(self.character, key)
        return attributes
