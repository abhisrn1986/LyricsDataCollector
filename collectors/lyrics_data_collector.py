import logging
import abc

from storages.lyrics_storage import LyricsStorage

logger = logging.getLogger(__name__)


class LyricsDataCollector(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'collect_lyrics_data') and
                callable(subclass.collect_lyrics_data) and
                hasattr(subclass, 'collect_artists') and
                callable(subclass.collect_artists) and
                hasattr(subclass, '__init__') and
                callable(subclass.__init__) and
                hasattr(subclass, 'source_url') and
                callable(subclass.source_url) and
                hasattr(subclass, 'get_lyrics_storage') and
                callable(subclass.get_lyrics_storage) or
                NotImplemented)

    @classmethod
    @abc.abstractclassmethod
    def source_url(cls) -> str:
        pass

    @abc.abstractclassmethod
    def __init__(self, lyrics_storage: LyricsStorage):
        pass

    @abc.abstractmethod
    def collect_lyrics_data(self, artist_names: list[str] = None):
        raise NotImplementedError

    @abc.abstractmethod
    def collect_artists(self, artist_names: list[str] = None):
        raise NotImplementedError

    @abc.abstractmethod
    def get_lyrics_storage(self) -> LyricsStorage:
        raise NotImplementedError
