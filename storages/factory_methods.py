import logging
from enum import Enum

from storages.lyrics_storage import LyricsStorage
from storages.lyrics_storage_csv import LyricsStorageCSV

logger = logging.getLogger(__name__)


class DataStorageType(Enum):

    DATA_STORAGE_CSV = 1


def create_storage(
        storage_type: DataStorageType, **storage_config_args) -> LyricsStorage:

    data_dir_arg_key = 'data_dir'
    if ((storage_type == DataStorageType.DATA_STORAGE_CSV) and
            (data_dir_arg_key in storage_config_args) and
            (storage_config_args[data_dir_arg_key] != 'data')):
        logger.info(
            f'''Created an instance of {LyricsStorageCSV.__name__} with
                {storage_config_args['data_dir']}''')
        return LyricsStorageCSV(storage_config_args['data_dir'])

    storage_config_args['data_dir'] = 'data'
    logger.info(
        f"Created an instance of {LyricsStorageCSV.__name__} with {storage_config_args['data_dir']}")
    return LyricsStorageCSV(storage_config_args['data_dir'])
