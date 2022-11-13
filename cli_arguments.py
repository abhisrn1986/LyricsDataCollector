import argparse
from collectors.factory_methods import DataCollectorType
from storages.factory_methods import DataStorageType


def get_cli_args():
    parser = argparse.ArgumentParser(
        description='''Run the script to collect and store the lyrics of
        various artists''')

    parser.add_argument(
        '--artists', type=str, nargs='+', required=True,
        help='''Provide a list of artists. Remember this should be a space 
        seperated. Remember to have an underscore \"_\" or a dash \"-\" 
        between each word or the artist name as shown below. For example : 
        --artists Linkin_Park Imagine_Dragons Cold_Play.''')

    parser.add_argument(
        '--data_collector_type', type=str, 
        default=DataCollectorType.LYRICS_COM_DATA_COLLECTOR.name,
        help=f'''Provide the type of collector to use. Possible types are
        {DataCollectorType._member_names_} Example:
         --data_collector_type {DataCollectorType.LYRICS_COM_DATA_COLLECTOR.name}''')

    parser.add_argument(
        '--data_storage_type', type=str,
        default=DataStorageType.DATA_STORAGE_CSV.name,
        help=f'''Provide the type of storage to use. Possible types are 
        {DataStorageType._member_names_} Example: 
        --data_collector_type {DataStorageType.DATA_STORAGE_CSV.name}''')

    parser.add_argument(
        '--data_storage_config', type=str,
        default="{\"data_dir\" : \"data\"}",
        help=f'''Provide a dict of parameters needed for the
        data storage used. {DataStorageType.DATA_STORAGE_CSV.name}
        type needs a relative or complete path with keyword data_dir''' + 
        "For example : --data_storage_config {\"data_dir\" : \"data2\"}.")

    args = parser.parse_args()

    return args
