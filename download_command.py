import os
import boto_session
import sys


def run(album, path):
    if not album:
        print("Вы не указали необходимую опцию --album", file=sys.stderr)
        sys.exit(1)
    s3 = boto_session.get_storage_client()
    bucket = boto_session.get_config('bucket')
    try:
        images = s3.list_objects_v2(Bucket=bucket, Prefix=f'{album}/').get('Contents', [])
        valid_images = (".jpg", ".jpeg")
        images = list(filter(lambda img: img['Key'].endswith(valid_images), images))
    except Exception:
        print("Произошла ошибка при получении фотографий", file=sys.stderr)
        sys.exit(1)
    if not images:
        print(f"Альбом {album} не существует или в нем нет фотографий", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        for image in images:
            photo_key = image['Key']
            photo_name = photo_key.split('/')[-1]
            photo_path = os.path.join(path, photo_name)
            s3.download_file(bucket, photo_key, photo_path)
            print("Успешно загружена фотография", photo_name)
        sys.exit(0)
    except Exception:
        print("Произошла ошибка во время загрузки фотографий или при доступе к каталогу", file=sys.stderr)
        sys.exit(1)
