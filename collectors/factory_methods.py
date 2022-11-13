
import logging
from enum import Enum


from storages.lyrics_storage import LyricsStorage

from collectors.lyrics_data_collector import LyricsDataCollector
from collectors.lyrics_com_data_collector import LyricsComDataCollector


class DataCollectorType(Enum):

    LYRICS_COM_DATA_COLLECTOR = 1


def create_collector(lyrics_storage: LyricsStorage, collector_type: DataCollectorType = DataCollectorType.LYRICS_COM_DATA_COLLECTOR,
                     ) -> LyricsDataCollector:

	if (collector_type == DataCollectorType.LYRICS_COM_DATA_COLLECTOR):
		logging.info(f"Created an instance of {LyricsComDataCollector.__class__}")
		return LyricsComDataCollector(lyrics_storage)

	logging.info(
	    f"Created a default instance of {LyricsComDataCollector.__class__}")
	return LyricsComDataCollector(lyrics_storage)
