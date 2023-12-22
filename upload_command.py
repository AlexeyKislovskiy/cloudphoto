import os
import boto_session
import sys


def get_images(path):
    images = []
    valid_images = (".jpg", ".jpeg")
    try:
        for file in os.listdir(path):
            if file.lower().endswith(valid_images):
                image = [file]
                file_path = os.path.join(path, file)
                with open(file_path, 'rb') as f:
                    byte_data = f.read()
                image.append(byte_data)
                images.append(image)
        if not images:
            print("В указанном каталоге нет фотографий", file=sys.stderr)
            sys.exit(1)
        return images
    except Exception:
        print("Произошла ошибка во время чтения фотографий или при доступе к каталогу", file=sys.stderr)
        sys.exit(1)


def run(album, path):
    if not album:
        print("Вы не указали необходимую опцию --album", file=sys.stderr)
        sys.exit(1)
    images = get_images(path)
    s3 = boto_session.get_storage_client()
    bucket = boto_session.get_config('bucket')
    try:
        s3.put_object(Bucket=bucket, Body=b'', Key=f"{album}/")
    except Exception:
        print("Произошла ошибка во время создания альбома", file=sys.stderr)
        sys.exit(1)
    for image in images:
        try:
            s3.put_object(Bucket=bucket, Key=f"{album}/{image[0]}", Body=image[1], ContentType='image/jpeg')
            print("Успешно отправлена фотография", image[0])
        except Exception:
            print("Произошла ошибка во время отправки фотографии", image[0], file=sys.stderr)
    sys.exit(0)
