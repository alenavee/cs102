import datetime as dt
from statistics import median
from typing import Optional

from api import get_friends
from api_models import User


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    friends_list = get_friends(user_id, 'bdate')
    age_list = []

    for friend in friends_list:
        user = User(**friend)
        if user.bdate is not None:
            bdate = user.bdate.split('.')
            if len(bdate) == 3:
                year = dt.datetime.now().year
                month = dt.datetime.now().month
                day = dt.datetime.now().day
                if (month >= int(bdate[1])) & (day >= int(bdate[0])):
                    age_list.append(year - int(bdate[2]))
                else:
                    age_list.append(year - int(bdate[2]) - 1)

    age_list.sort()

    if len(age_list) != 0:
        age = median(age_list)
    else:
        age = None
    return age

if __name__ == '__main__':
    predicted_age = age_predict(83798048)
    print(predicted_age)