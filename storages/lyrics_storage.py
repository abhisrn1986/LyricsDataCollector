import logging
import abc

import pandas as pd

logger = logging.getLogger(__name__)

SONG_NAME_LABEL = 'song_title'
LYRICS_COL_LABEL = 'lyrics'
SONG_LINK_COL_LABEL = 'link'
TARGET_LABEL = 'artist'


class LyricsStorage(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'store_artist_lyrics') and
                callable(subclass.store_artist_lyrics) and
                hasattr(subclass, 'get_unstored_song_names') and
                callable(subclass.get_unstored_song_names) and
                hasattr(subclass, 'get_lyrics_data') and
                callable(subclass.get_lyrics_data) or
                NotImplemented)

    @abc.abstractmethod
    def store_artist_lyrics(self, artist_name: str,
                            artist_lyrics_df: pd.DataFrame) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def get_unstored_song_names(
            self, artist_name: str, song_names: pd.Series) -> pd.Series:
        raise NotImplementedError

    @abc.abstractmethod
    def get_lyrics_data(self, artist_names: list[str]) -> pd.DataFrame:
        raise NotImplementedError
