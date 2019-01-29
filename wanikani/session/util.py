import datetime

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
