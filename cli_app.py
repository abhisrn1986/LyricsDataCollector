# from xml.parsers.expat import model
import re
import os.path
from os import mkdir
import logging

import json
from cli_arguments import get_cli_args

from collectors.factory_methods import create_collector, DataCollectorType
from storages.factory_methods import create_storage, DataStorageType

# Initialize the data folder to store the model and lyrics files
dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"

# specify the logging level
logging.basicConfig(encoding='utf-8', level=logging.INFO)

if __name__ == "__main__":

    # Process and get the cli arguments.
    args = get_cli_args()

    storage_config_params = {}
    if args.data_storage_config is not None:
        storage_config_params = json.loads(args.data_storage_config)
    storage = create_storage(
        DataStorageType[args.data_storage_type],
        **storage_config_params)

    data_collector = create_collector(
        storage, DataCollectorType[args.data_collector_type])

    logging.info(f"Collecting lyrics data for {args.artists}")
    data_collector.collect_lyrics_data(args.artists)
    logging.info(f"Collection of lyrics data for {args.artists}")
