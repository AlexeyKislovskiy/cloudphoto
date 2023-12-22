import boto_session
import sys


def run(album):
    s3 = boto_session.get_storage_client()
    bucket = boto_session.get_config('bucket')

    if not album:
        albums = [album['Prefix'].rstrip('/') for album in
                  s3.list_objects_v2(Bucket=bucket, Delimiter='/')['CommonPrefixes']]
        if not albums:
            print("В облачном хранилище нет альбомов", file=sys.stderr)
            sys.exit(1)
        for album in albums:
            print(album)

    else:
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
        else:
            for image in images:
                image_key = image['Key']
                image_name = image_key.split('/')[-1]
                print(image_name)

    sys.exit(0)
