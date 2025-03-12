from spotifylayer.helper_types import TrimmedPlaylist


def parse_user(response: dict) -> dict:
    """
    Parse JSON response for spotify api call /me (current_user())
    :param response: JSON response from sp.current_user()
    :return: response data formatted as dict which can be directly passed to SpotifyUser model
    :rtype: dict
    """
    return {
        'display_name': response['display_name'],
        'spotify_id': response['id'],
        'spotify_uri': response['uri'],
        'profile_image': response['images'][0]['url'],
    }


def playlist_from_recently_played(response: dict) -> list:
    """
    Parse JSON response for spotify api call /me/player/recently-played
    :param response: JSON response from sp.current_user_recently_played()
    :return: list of playlist URIs
    :rtype: list
    """
    uris = []

    for item in response['items']:
        if item['context'] is not None and item['context']['type'] == 'playlist':
            uris.append(item['context']['uri'])

    return uris

def parse_user_playlists(response: dict) -> list:
    """
    Parse JSON response for spotify api call /me/playlists
    :param response: JSON response from sp.current_user_playlists()
    :return: list of playlist objects
    :rtype: list
    """
    playlists = []

    for item in response['items']:
        playlists.append(TrimmedPlaylist(**{
            'href': item['href'],
            'description': item['description'],
            'spotify_id': item['id'],
            'name': item['name'],
            'spotify_uri': item['uri'],
            'image_url': item['images'][0]['url'] if item['images'] else None,
        }))

    return playlists