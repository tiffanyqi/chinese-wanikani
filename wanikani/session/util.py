import datetime
import json

from wanikani.models import BaseCharacter, ProgressCharacter

def get_upcoming_review_date(now, level):
    """
    Wanikani's SRS system separates each level by the following hours: 4, 4, 16, 24, 48, 240, 384, 2160
    To make the logic a bit more simple, the hours here will increment by a multiple of 2, such as:
        2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048
    When the user passes the 11th level, it will be considered burned and removed from the queue.
    """
    base_hour = 2
    hours_from_now = base_hour ** level
    next_date = now + datetime.timedelta(hours=hours_from_now)
    return next_date.replace(microsecond=0, second=0, minute=0) # rounds down

def get_level(character):
    """
    There is also a penalty factor in which reduces the level further depending on how many times you answer
    incorrectly in a given session.
    """
    # TODO: add a penalty factor to further decrease the more times a user answers incorrectly
    if character.num_current_incorrect['pinyin'] > 0 or character.num_current_incorrect['definitions'] > 0:
        return character.level - 1 if character.level > 1 else 1
    else:
        return character.level + 1


def check_level_up(user):
    """
    Checks whether the user is ready to move onto the next user level.
    This threshold is made when 90% of the characters' levels are 5 or above.
    """
    character_objects = ProgressCharacter.objects.filter(user=user, user__level=user.level)
    characters_leveled = character_objects.filter(level__gte=5)
    return (characters_leveled.count() / character_objects.count()) > 0.9


def level_up(user):
    """
    Levels up the user.
    """
    user.level += 1
    generate_characters_for_level(user)
    user.save()


def generate_characters_for_level(user):
    """
    Creates a set of characters directly related to the user's progress
    """
    characters = BaseCharacter.objects.filter(user_level=user.level)
    now = datetime.datetime.now()
    for character in characters:
        ProgressCharacter.objects.create(
            character=character,
            num_correct={'pinyin': 0, 'definitions': 0, 'all': 0},
            num_current_incorrect={'pinyin': 0, 'definitions': 0},
            unlocked_date=now,
            user=user,
        ).save()
