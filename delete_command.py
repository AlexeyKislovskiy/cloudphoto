import boto_session
import sys


def run(album, photo):
    if not album:
        print("Вы не указали необходимую опцию --album", file=sys.stderr)
        sys.exit(1)
    s3 = boto_session.get_storage_client()
    bucket = boto_session.get_config('bucket')

    if not photo:
        try:
            s3.head_object(Bucket=bucket, Key=f'{album}/')
        except s3.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                print(f"Альбом {album} не существует", file=sys.stderr)
                sys.exit(1)
            else:
                print(f'Произошла ошибка при получении альбома', file=sys.stderr)
                sys.exit(1)

        images_to_delete = []
        try:
            images = s3.list_objects_v2(Bucket=bucket, Prefix=f'{album}/').get('Contents', [])
        except Exception:
            print("Произошла ошибка при получении фотографий для удаления", file=sys.stderr)
            sys.exit(1)
        for image in images:
            images_to_delete.append({'Key': image['Key']})
        images_to_delete.append({'Key': f'{album}/'})
        try:
            s3.delete_objects(Bucket=bucket, Delete={'Objects': images_to_delete})
            print(f'Альбом {album} и все фотографии в нем успешно удалены')
        except Exception:
            print("Произошла ошибка при удалении фотографий", file=sys.stderr)
            sys.exit(1)

    else:
        try:
            s3.head_object(Bucket=bucket, Key=f'{album}/{photo}')
        except s3.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                print(f'Фотография {photo} не найдена в альбоме {album}', file=sys.stderr)
                sys.exit(1)
            else:
                print(f'Произошла ошибка при получении фотографии', file=sys.stderr)
                sys.exit(1)
        try:
            s3.delete_object(Bucket=bucket, Key=f'{album}/{photo}')
            print(f'Фотография {photo} успешно удалена из альбома {album}')
        except Exception:
            print("Произошла ошибка при удалении фотографии", file=sys.stderr)
            sys.exit(1)

    sys.exit(0)
