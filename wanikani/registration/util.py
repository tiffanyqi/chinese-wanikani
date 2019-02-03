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
