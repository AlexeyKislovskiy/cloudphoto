import os
import configparser
import boto_session
import sys


def run():
    config = configparser.ConfigParser()
    aws_access_key_id = input("Введите ваш AWS access key ID: ")
    aws_secret_access_key = input("Введите ваш AWS secret access key: ")
    bucket = input("Введите имя вашего бакета: ")
    config['DEFAULT'] = {
        'bucket': bucket,
        'aws_access_key_id': aws_access_key_id,
        'aws_secret_access_key': aws_secret_access_key,
        'region': 'ru-central1',
        'endpoint_url': 'https://storage.yandexcloud.net'
    }
    config_file_path = os.path.join(os.path.expanduser('~'), '.config', 'cloudphoto', 'cloudphotorc')

    try:
        os.makedirs(os.path.dirname(config_file_path), exist_ok=True)
        with open(config_file_path, 'w') as configfile:
            config.write(configfile)
        print("Значения параметров успешно сохранены в конфигурационном файле", config_file_path)
    except Exception:
        print("Произошла ошибка во время создания конфигурационного файла", file=sys.stderr)
        sys.exit(1)

    try:
        s3 = boto_session.get_storage_client()
        s3.head_bucket(Bucket=bucket)
        print(f'Бакет с именем {bucket} уже существует')
        sys.exit(0)
    except s3.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            s3 = boto_session.get_storage_client()
            s3.create_bucket(Bucket=bucket, ACL='public-read')
            print("Успешно создан бакет с именем", bucket)
            sys.exit(0)
        else:
            print("Произошла ошибка во время создания бакета", file=sys.stderr)
            sys.exit(1)
