import datetime

from wanikani.models import BaseCharacter, ProgressCharacter, Session, User


def save_user(username, password, email):
    """
    Saves a user in the database.
    """
    user_object = User.objects.create(
        username=username,
        password=password,
        email=email,
        level=1,
    )
    user_object.save()
    return user_object


def setup_characters(user):
    """
    Creates a set of characters directly related to the user's progress
    """
    characters = BaseCharacter.objects.filter(user_level=user.level)
    now = datetime.datetime.now()
    for character in characters:
        ProgressCharacter.objects.create(
            user=user,
            character=character,
            unlocked_date=now,
        ).save()
