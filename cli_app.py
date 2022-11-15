import json

import custom_logger
from cli_arguments import get_cli_args
from collectors.factory_methods import create_collector, DataCollectorType
from storages.factory_methods import create_storage, DataStorageType

logger = custom_logger.get_custom_named_logger(__name__)


if __name__ == "__main__":

    # Process and get the cli arguments.
    args = get_cli_args()

    # Create a storage type.
    storage_config_params = {}  # parameters for the data storage used.
    if args.data_storage_config is not None:
        storage_config_params = dict(args.data_storage_config)
    storage = create_storage(
        DataStorageType[args.data_storage_type],
        **storage_config_params)

    # Create a collector.
    data_collector = create_collector(
        storage, DataCollectorType[args.data_collector_type])

    # Collecte the data.
    logger.info(f"Collecting lyrics data for {args.artists}.....")
    data_collector.collect_lyrics_data(args.artists)
    logger.info(f"Collected of lyrics data for {args.artists}")
