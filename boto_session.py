import boto3
import os
import configparser
import sys


def get_config(field_name):
    config = configparser.ConfigParser()
    config_file_path = os.path.join(os.path.expanduser('~'), '.config', 'cloudphoto', 'cloudphotorc')
    try:
        config.read(config_file_path)
        return config.get('DEFAULT', field_name)
    except (configparser.NoSectionError, configparser.NoOptionError, FileNotFoundError):
        print("Конфигурационный файл отсутствует или заполнен неправильно", file=sys.stderr)
        sys.exit(1)


def get_boto_session():
    aws_access_key_id = get_config('aws_access_key_id')
    aws_secret_access_key = get_config('aws_secret_access_key')
    return boto3.session.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )


def get_storage_client():
    endpoint_url = get_config('endpoint_url')
    region = get_config('region')
    return get_boto_session().client(
        service_name='s3',
        endpoint_url=endpoint_url,
        region_name=region
    )


def get_resource():
    endpoint_url = get_config('endpoint_url')
    region = get_config('region')
    return get_boto_session().resource(
        service_name='s3',
        endpoint_url=endpoint_url,
        region_name=region
    )
