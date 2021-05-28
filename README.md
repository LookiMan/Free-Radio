# Free-Radio


**Несколько слов о радио**

Простое и удобное радио с возможностью добавления новых радиостанций.

**Важно.** Для работы данной программы необходимо установить **VLC media player.**


<hr>


В папке Free-Radio-Executable находится полностью готовая к использованию программа, скомпилированная с помощью [easycompiller](https://github.com/topdefaultuser/easycompiller).

Версия ```python 3.7.1```, компилятор ```PyInstaller```. 

Команда для компиляции: ```python -m PyInstaller -y  -F -w --noupx -i"images\icon.ico" "main.py"```

Хеш-сумма:

MD5: 112DE5BAB07F36F0EB4DF85493D229BF

SHA-256: 20EA3783DE415F398FEBFBDCDB25C51D0D115212495A1EB1E5CD57F5C9B74C72


Можно декомпилировать приложение с помощью [EXE2PY-Decompiler](https://github.com/topdefaultuser/EXE2PY-Decompiler).


<hr>


**Примечания**


Если возникает ошибка при запуске *скомпилированного*  приложения.

![]( https://github.com/topdefaultuser/Free-Radio/blob/main/Screenshots/ERROR.PNG)

В окне проводника перейдите по пути: C:\Users\%USERNAME%\radio\ (если папка radio не существует, создайте ее)

Если в данной папке нет файла под именем "radios.json", вручную скопируйте файл "radios.json" с папки data
которая находится в папке Free-Radio-Executable.

По желанию можно изменить задний фон заменив изображение background_image.png на своё.

<hr>


**Скриншоты**


_Главное окно радио_

![]( https://github.com/topdefaultuser/Free-Radio/blob/main/Screenshots/MainForm.PNG)


_Окно выбора радиостанции_

![]( https://github.com/topdefaultuser/Free-Radio/blob/main/Screenshots/SelectRadioStationForm.PNG)


_Окно добавления новой радиостанции_

![]( https://github.com/topdefaultuser/Free-Radio/blob/main/Screenshots/AppendStationForm.PNG)
