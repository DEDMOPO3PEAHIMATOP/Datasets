# Datasets
Програмка для создания датасета из фотографий.
Для работы проекта необходим python 3.7 и выше + библиотека tkinter

Для начала скачйте папку с проектом на свою машину.

Возможна установка и запуск через запуск

# run.sh

Либо вручную по данному алгоритму:

Настоятельно рекомендую создать папку с виртуальным окружением в папке с проектом:

# python -m venv myenv

И запуститься в нем:

# source myenv/bin/activate

либо

# source myenv/Scripts/activate

В запущенной виртуальном окружении установите зависимости:

# pip install -r requirements.txt

И запускайтесь:

# python main.py

## Работа с программой

1. Установите путь для обработанных фотографий ("Папка для обработанных фотографий" -> "Выбрать").
2. В левом окне выберите директорию, с которой будете работать.
3. При выборе файла в левом окне, в правом окне будут появляться изображения из выбранного файла.
4. Если вы классифицировали животное по фото, можно записать его вид в поле "Вид животного".
5. Установить его пол в поле "Пол животного".
6. Установить его возраст в поле "Возраст животного".
7. И нажать "Обработать".
8. При нажатии на клавишу "Обработать" переименованый файл переместится в выбранноу ранее директорию для обработанных фото.
9. Можно приступать к классификации следующего фото.
