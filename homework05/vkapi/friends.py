import dataclasses
import math
import time
import typing as tp

from vkapi import session, config

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]

#test done
@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    '''
    Ответ на вызов метода `friends.get`.
    :param count: Количество пользователей.
    :param items: Список идентификаторов друзей пользователя или список пользователей.
    '''
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


'''
    get_friends: получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).
'''


def get_friends(
        user_id: int,  # Идентификатор пользователя, список друзей для которого нужно получить.
        count: int = 5000,  # Количество друзей, которое нужно вернуть.
        offset: int = 0,  # Смещение, необходимое для выборки определенного подмножества друзей.
        fields: tp.Optional[tp.List[str]] = None  # Список полей, которые нужно получить для каждого пользователя.
) -> FriendsResponse:
    response = session.get(
        'friends.get',
        params={
            'user_id': user_id,
            'count': count,
            'offset': offset,
            'fields': fields,
            'access_token': config.VK_CONFIG['access_token'],
            'v': config.VK_CONFIG['version'],
        },
    ).json()['response']  # парсинг
    # Список идентификаторов друзей пользователя или список пользователей.
    return FriendsResponse(count=response['count'], items=response['items'])


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int

    '''
    Получить список идентификаторов общих друзей между парой пользователей.
    '''


def get_mutual(
        source_uid: tp.Optional[int] = None,
        # Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
        target_uid: tp.Optional[int] = None,  # Идентификатор пользователя, с которым необходимо искать общих друзей.
        target_uids: tp.Optional[tp.List[int]] = None,  # type: ignore
        # Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
        order: str = '',  # Порядок, в котором нужно вернуть список общих друзей.
        count: tp.Optional[int] = None,  # Количество общих друзей, которое нужно вернуть.
        offset: int = 0,  # Смещение, необходимое для выборки определенного подмножества общих друзей.
        progress=None,  # Callback для отображения прогресса.
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    if target_uid is not None:
        return session.get(
            'friends.getMutual',
            params={
                'source_uid': source_uid,
                'target_uid': target_uid,
                'order': order,
                'count': count,
                'offset': offset,
                'access_token': config.VK_CONFIG['access_token'],
                'v': config.VK_CONFIG['version'],
            },
        ).json()['response']

    result: tp.List[MutualFriends] = []
    range_ = range(0, len(target_uids), 100)  # type: ignore
    if progress is not None:
        range_ = progress(range_)

    for cursor in range_:
        response = session.get(
            'friends.getMutual',
            params={
                'source_uid': source_uid,
                'target_uids': ','.join([str(i) for i in target_uids[cursor: cursor + 100]]),  # type: ignore
                'order': order,
                'count': count,
                'offset': offset + cursor,
                'access_token': config.VK_CONFIG['access_token'],
                'v': config.VK_CONFIG['version'],
            },
        ).json()['response']
        result.extend(
            MutualFriends(
                id=data['id'],
                common_friends=data['common_friends'],
                common_count=data['common_count'],
            )
            for data in response
        )
        time.sleep(1 / 3 + 0.01)

    return result
