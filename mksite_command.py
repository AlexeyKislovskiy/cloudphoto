import boto_session
import sys
import json


def run():
    s3 = boto_session.get_storage_client()
    bucket = boto_session.get_config('bucket')
    try:
        s3.put_bucket_website(
            Bucket=bucket,
            WebsiteConfiguration={
                'IndexDocument': {'Suffix': 'index.html'},
                'ErrorDocument': {'Key': 'error.html'}
            }
        )
        albums = [album['Prefix'].rstrip('/') for album in
                  s3.list_objects_v2(Bucket=bucket, Delimiter='/')['CommonPrefixes']]
        index_html = index_html_top
        for i, album in enumerate(albums):
            album_number = i + 1
            index_html += f'<li><a href="album{album_number}.html">{album}</a></li>'
            album_html = album_html_top
            images = s3.list_objects_v2(Bucket=bucket, Prefix=f'{album}/').get('Contents', [])
            valid_images = (".jpg", ".jpeg")
            images = list(filter(lambda img: img['Key'].endswith(valid_images), images))
            for image in images:
                image_key = image['Key']
                album_html += f'<img src="https://storage.yandexcloud.net/{bucket}/{image_key}" data-title="{image}">'
            album_html += album_html_bottom
            s3.put_object(Bucket=bucket, Key=f'album{album_number}.html', Body=album_html)
        index_html += index_html_bottom
        s3.put_object(Bucket=bucket, Key='index.html', Body=index_html)
        s3.put_object(Bucket=bucket, Key='error.html', Body=error_html)
        print(
            f'Веб-страницы фотоархива успешно созданы и опубликованы. Ссылка на сайт: http://{bucket}.website.yandexcloud.net/')
        sys.exit(0)
    except Exception:
        print("Произошла ошибка при создании веб-страниц фотоархива", file=sys.stderr)
        sys.exit(1)


error_html = """
<!doctype html>
<html>
    <head>
        <title>Фотоархив</title>
    </head>
<body>
    <h1>Ошибка</h1>
    <p>Ошибка при доступе к фотоархиву. Вернитесь на <a href="index.html">главную страницу</a> фотоархива.</p>
</body>
</html>
"""

index_html_top = """
<!doctype html>
<html>
    <head>
        <title>Фотоархив</title>
    </head>
<body>
    <h1>Фотоархив</h1>
    <ul>
"""

index_html_bottom = """
    </ul>
</body
"""

album_html_top = """
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/galleria/1.6.1/themes/classic/galleria.classic.min.css" />
        <style>
            .galleria{ width: 960px; height: 540px; background: #000 }
        </style>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/galleria/1.6.1/galleria.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/galleria/1.6.1/themes/classic/galleria.classic.min.js"></script>
    </head>
    <body>
        <div class="galleria">
"""

album_html_bottom = """
        </div>
        <p>Вернуться на <a href="index.html">главную страницу</a> фотоархива</p>
        <script>
            (function() {
                Galleria.run('.galleria');
            }());
        </script>
    </body>
</html>
"""
