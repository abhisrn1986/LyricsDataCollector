import logging
import threading
import re
from tqdm import tqdm

import requests
from bs4 import BeautifulSoup
import pandas as pd

from storages.lyrics_storage import LyricsStorage, SONG_NAME_LABEL, LYRICS_COL_LABEL, SONG_LINK_COL_LABEL
from collectors.lyrics_data_collector import LyricsDataCollector


logger = logging.getLogger(__name__)


class AtomicTqdm(tqdm):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self._lock = threading.Lock()

    def update(self, n=1):
        with self._lock:
            super().update(n)


def update_tqdm(func):

    def tqdm_func(*args, **kwargs):
        func(*args)
        # still needs to check the threading locking issue
        # to uncomment this.
        # kwargs['progress'].update(n=1)

    return tqdm_func


class LyricsComDataCollector(LyricsDataCollector):

    @classmethod
    def __class__(cls) -> str:
        return 'LyricsComDataCollector'

    @classmethod
    def source_url(cls) -> str:
        return 'https://www.lyrics.com'

    @classmethod
    def parser_for_soup(cls) -> str:
        return 'lxml'

    def __init__(self, lyrics_storage: LyricsStorage) -> None:
        self.lyrics_storage = lyrics_storage
        self.parser_for_soup = self.parser_for_soup()

    def collect_artists(self, artist_names: list[str] = None):
        pass

    def collect_lyrics_data(self, artist_names: list[str] = None):
        # Extract the songs to data frames if there is a csv file else
        # web scrape the songs from the lyrics.com
        progress_bar = tqdm(total=len(artist_names),
                            desc=f"Collecting artists lyrics")
        for i, artist in enumerate(artist_names):

            progress_bar.desc = f"Collected artist {artist_names[i]} lyrics"

            songs_df = self.get_songs(artist)
            songs_to_extract = self.lyrics_storage.get_unstored_song_names(
                artist, songs_df[SONG_NAME_LABEL])
            songs_df = songs_df.loc[songs_df[SONG_NAME_LABEL].isin(
                songs_to_extract)]

            songs_df = self.extract_lyrics(songs_df)

            self.lyrics_storage.store_artist_lyrics(artist, songs_df)

            progress_bar.update(n=1)

    def get_lyrics_storage(self) -> LyricsStorage:
        return self.lyrics_storage

    @classmethod
    @update_tqdm
    def extract_lyrics_from_url(cls, songs, i):
        try:
            soup = BeautifulSoup(requests.get(
                cls.source_url()).text, cls.parser_for_soup())
        except Exception as e:
            logging.warn(
                f"Exception {e} occured while downloading from url {cls.source_url()} skipping this song!")
        lyrics = ""
        lyrics_tag = soup.find('pre', attrs={'id': 'lyric-body-text'})
        if lyrics_tag:
            for child in lyrics_tag.children:
                lyrics += child.text
        songs[i] = lyrics
        # extract_lyrics_from_url.atomic_tqdm.update()

    def get_songs(self, artist) -> pd.DataFrame:
        src_url = self.source_url()
        artist_url = f'{src_url}/artist/{artist}'
        artist_html = requests.get(artist_url).text

        try:
            soup = BeautifulSoup(artist_html, features=self.parser_for_soup)
        except Exception as e:
            raise RuntimeError(
                f'Exception {e} occured while extracting song links for artist {artist} skipping this artist!')

        # Get all the song titles and the links to their respective lyrics
        songs = dict()
        square_bracket_pattern = ' \[.*\]'
        # for song in soup.find_all('strong'):

        songs_elements = soup.find_all('td', attrs={'class': 'tal qx'})
        if len(songs_elements) == 0:
            logging.warn(
                f'No song links found for artist {artist} and hence skipping this artist!')
        for song in songs_elements:
            a = song.find('strong').find('a')
            if a and not (re.findall(square_bracket_pattern, a.text)):
                songs[a.text.lower()] = src_url + a.get('href')
        songs_df = pd.DataFrame(columns=[SONG_NAME_LABEL, SONG_LINK_COL_LABEL])
        songs_df[SONG_NAME_LABEL] = songs.keys()
        songs_df[SONG_LINK_COL_LABEL] = songs.values()
        return songs_df

    def extract_lyrics(self, songs_df):

        # Each thread extracts lyrics from each url
        all_lyrics = [None] * songs_df[SONG_LINK_COL_LABEL].shape[0]

        # Create a thread for extracting each song of the current artist
        threads = []
        # atomic_tqdm = AtomicTqdm(total=len(all_lyrics), desc=f"Collecting artists lyrics")
        # kwargs={'progress': atomic_tqdm}
        for index, url in enumerate(songs_df[SONG_LINK_COL_LABEL].values):
            t = threading.Thread(target=self.extract_lyrics_from_url,
                                 args=[all_lyrics, index])
            #  args=[all_lyrics, index], kwargs=kwargs)
            t.start()
            threads.append(t)

        # Wait for all the songs to be downloaded.
        for thread in threads:
            thread.join()

        songs_df[LYRICS_COL_LABEL] = all_lyrics

        # drop rows for any song for which lyrics were not extracted.
        songs_df.dropna()

        return songs_df
