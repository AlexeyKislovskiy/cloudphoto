# cloudphoto
 Для сборки выполните setup.sh и обновите содержимое файла .bashrc, чтобы добавить cloudphoto в PATH:
 ```
 bash setup.sh
 source ~/.bashrc
 ```
 После чего можно будет запускать программу cloudphoto следующим образом:
 ```
cloudphoto COMMAND [OPTIONS]...
```
В программе содержатся 3 директории с изображениями для быстрого теста программы:
```
cloudphoto init
cloudphoto upload --album fruits --path fruits
cloudphoto upload --album fruits --path fruits
cloudphoto upload --album vegetables --path vegetables
cloudphoto upload --album berries --path berries
cloudphoto mksite
```
