from dataclasses import dataclass
from typing import Optional, Union, List

@dataclass
class TrimmedTrack:
    """
    Track representation with the minimum amount of data needed to display it in a list. Used in the liked_songs view.
    """
    name: str
    artists: List[str]
    album: str
    release_date: str


@dataclass
class TrimmedPlaylist:
    """
    Playlist representation with the minimum amount of data needed to display it in a list.
    """
    href: str
    description: Union[str, None]
    spotify_id: str
    name: str
    spotify_uri: str
    image_url: Union[str, None]
