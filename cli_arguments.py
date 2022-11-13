import argparse
from collectors.factory_methods import DataCollectorType
from storages.factory_methods import DataStorageType


def key_value(s):
    try:
        x, y = map(str, s.split(','))
        return (x, y)
    except RuntimeError as e:
        raise argparse.ArgumentTypeError(
            "The key and value should be (key, value)")


def get_cli_args():
    parser = argparse.ArgumentParser(
        description='''Run the script to collect and store the lyrics of
        various artists''')

    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument(
        '--artists', type=str, nargs='+', required=True,
        help='''Provide a list of artists. Remember this should be a space 
        seperated. Remember to have an underscore \"_\" or a dash \"-\" 
        between each word or the artist name as shown below. For example : 
        --artists Linkin_Park Imagine_Dragons Cold_Play.''')

    optional_args = parser.add_argument_group('optional arguments')

    optional_args.add_argument(
        '--data_collector_type', type=str,
        default=DataCollectorType.LYRICS_COM_DATA_COLLECTOR.name,
        help=f'''Provide the type of collector to use. Possible types are
        {DataCollectorType._member_names_} Example:
         --data_collector_type {DataCollectorType.LYRICS_COM_DATA_COLLECTOR.name}''')

    optional_args.add_argument(
        '--data_storage_type', type=str,
        default=DataStorageType.DATA_STORAGE_CSV.name,
        help=f'''Provide the type of storage to use. Possible types are 
        {DataStorageType._member_names_} Example: 
        --data_collector_type {DataStorageType.DATA_STORAGE_CSV.name}''')

    optional_args.add_argument(
        '--data_storage_config', type=key_value, nargs='*',
        help=f'''Provide a dict of parameters needed for the
        data storage used. {DataStorageType.DATA_STORAGE_CSV.name}
        type needs a relative or complete path with keyword data_dir''' +
        '''For example : --data_storage_config data_dir,data2
           Example with multiple keyvalues : 
           --data_storage_config key1,value1 key2,value2 .......''')

    args = parser.parse_args()

    return args
