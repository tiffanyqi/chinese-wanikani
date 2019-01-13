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
    character = models.CharField(null=True, max_length=50)
    definitions = JSONField()
    pinyin = JSONField()
    hsk_level = models.IntegerField(default=0)
    frequency = models.IntegerField(default=0)
    user_level = models.IntegerField(default=0)


class LevelCharacter(models.Model):
    character = models.ForeignKey(BaseCharacter, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unlocked = models.BooleanField(default=False)
    num_correct_pinyin = models.IntegerField(default=0)
    num_correct_definitions = models.IntegerField(default=0)
    num_correct_all = models.IntegerField(default=0)
    num_times_shown = models.IntegerField(default=0)
    unlocked_date = models.DateTimeField(default=None, null=False)
    upcoming_review_date = models.DateTimeField(default=None, null=False)
    last_reviewed_date = models.DateTimeField(default=None, null=False)
    last_session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True)
