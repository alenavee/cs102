import requests
import time

import config

domain = config.VK_CONFIG['domain']
access_token = config.VK_CONFIG['access_token']
version = config.VK_CONFIG['version']
username = config.PLOTLY_CONFIG['username']
api_key = config.PLOTLY_CONFIG['api_key']


def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос
    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    for i in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=timeout)
            return response
        except:
            if i == max_retries - 1:
                raise
            backoff = backoff_factor * (2 ** i)
            time.sleep(backoff)


def get_friends(user_id, fields):
    """ Вернуть данных о друзьях пользователя
    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    query_params = {
        'domain': domain,
        'access_token': access_token,
        'user_id': user_id,
        'fields': fields,
        'version': version
    }

    query = "{domain}/friends.get?access_token={" \
            "access_token}&user_id={user_id}&fields={fields}&v={version}".format(
        **query_params)
    response = get(query, query_params)
    err = response.json().get('error')
    if err:
        return []
    return response.json()['response']['items']