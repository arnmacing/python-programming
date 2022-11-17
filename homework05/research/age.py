import contextlib
import datetime as dt
import statistics
import typing as tp

from dateutil.relativedelta import relativedelta
from vkapi.friends import get_friends


# test done
def age_predict(user_id: int) -> tp.Optional[float]:
    ages = []
    friends = get_friends(user_id, fields=['bdate'])
    for friend in friends.items:
        with contextlib.suppress(KeyError, ValueError):
            bdate = dt.datetime.strptime(friend['bdate'], '%d.%m.%Y')  # type: ignore
            age = relativedelta(dt.datetime.now(), bdate).years
            ages.append(age)
    return statistics.median(ages) if ages else None
