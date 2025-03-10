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
