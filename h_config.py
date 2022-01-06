__DEFAULT_CONFIG_FILE_LOCATION = r'./config.yaml'
__GLOBAL_CONFIGURATION = None


def __read_configuration_file():
    global __DEFAULT_CONFIG_FILE_LOCATION
    with open(__DEFAULT_CONFIG_FILE_LOCATION, 'r') as configuration_file:
        print(f'Loading configuration from f{__DEFAULT_CONFIG_FILE_LOCATION}')
        import yaml
        return yaml.full_load(configuration_file)


def get_global_configuration():
    global __GLOBAL_CONFIGURATION
    return __GLOBAL_CONFIGURATION


def __configure_h_logger(configuration):
    print(f'Configuring logging \n {configuration}')
    import logging.config
    logging.config.dictConfig(configuration)


def configure():
    print('String App Configuration')
    global __GLOBAL_CONFIGURATION
    __GLOBAL_CONFIGURATION = __read_configuration_file()
    __configure_h_logger(__GLOBAL_CONFIGURATION['logging'])
