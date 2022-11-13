import logging
from enum import Enum


from storages.lyrics_storage import LyricsStorage
from storages.lyrics_storage_csv import LyricsStorageCSV


class DataStorageType(Enum):

    DATA_STORAGE_CSV = 1


def create_storage(
        storage_type: DataStorageType = DataStorageType.DATA_STORAGE_CSV, **
        storage_args) -> LyricsStorage:

	if (storage_type == DataStorageType.DATA_STORAGE_CSV):
		data_dir_arg = 'data_folder'
		if data_dir_arg in storage_args:
			logging.info(
			    f"Created an instance of {LyricsStorageCSV.__class__} with {storage_args[data_dir_arg]}")

			return LyricsStorageCSV(storage_type[data_dir_arg])

	default_data_dir = 'data'
	logging.info(
	    f"Created a default instance of {LyricsStorageCSV.__class__} with {default_data_dir}")
	return LyricsStorageCSV(default_data_dir)
