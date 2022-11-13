import re
import os
import logging

import pandas as pd

from storages.lyrics_storage import LyricsStorage, TARGET_LABEL, SONG_NAME_LABEL


class LyricsStorageCSV(LyricsStorage):
    def __init__(self, lyrics_data_dir: str) -> None:
        self.lyrics_data_dir = lyrics_data_dir
        if not os.path.exists(lyrics_data_dir):
            os.makedirs(self.lyrics_data_dir, exist_ok=True)

    def store_artist_lyrics(
            self, artist_name: str, lyrics_df: pd.DataFrame) -> bool:

        artist_name = re.sub('[ -]', "_", artist_name).lower()
        if artist_name == '':
            raise ValueError("Artist name is invalid")
        if not lyrics_df.empty:
            artist_filepath = os.path.join(
                self.lyrics_data_dir, artist_name+'.csv')

            if not os.path.exists(artist_filepath):
                lyrics_df.to_csv(artist_filepath, index=False, header=True)
            else:
                lyrics_df.to_csv(artist_filepath+'.csv')
                lyrics_df.to_csv(artist_filepath, mode='a',
                                 index=False, header=False)

            return True

        return False

    def get_unstored_song_names(
            self, artist_name: str, song_names: pd.Series) -> pd.Series:

        artist_name = re.sub('[ -]', "_", artist_name).lower()
        if artist_name == '':
            raise ValueError("Artist name is invalid")

        if not song_names.empty:
            artist_filepath = os.path.join(
                self.lyrics_data_dir, artist_name+'.csv')

            if not os.path.exists(artist_filepath):
                return song_names

            old_lyrics_df = pd.read_csv(artist_filepath)
            diff_song_names = song_names[~song_names.isin(
                old_lyrics_df[SONG_NAME_LABEL])]
            return diff_song_names

        return pd.Series()

    def get_lyrics_data(self, artist_names: list[str]) -> pd.DataFrame:

        artist_dfs = []
        for artist_name in artist_names:
            artist_name = re.sub('[ -]', "_", artist_name).lower()
            artist_filepath = os.path.join(
                self.lyrics_data_dir, artist_name+'.csv')

            if not os.path.exists(artist_filepath):
                logging.warn(
                    f'Data for artist {artist_name} is not found in the storage')
                continue

            artist_df = pd.read_csv(artist_filepath)
            artist_df[TARGET_LABEL] = artist_name
            artist_dfs.append(artist_df)

        return pd.concat(artist_dfs, ignore_index=True)
