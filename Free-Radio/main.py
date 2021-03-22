import sys
import os

import vlcplayerdriver
import ui
import utils


"""

В модуле vlcmediplayer реализован класс VlcPlayerDriver выступающий в роли надстройки над
библтотекой vlc(управляющей установленым в системе Vlc Media Player).

В модуле ui реализованы классы Widget, Playlist, AppendStationForm,
выступающий в роли UI.

Вся логика необходимая для работы радио реализована в функциях play, pause, stop,
mute_switch, change_volume, set_radio_station_by_name, change_radio_station,
prev_radio_station и next_radio_station.

"""


def play(widget, player):
    widget.playButton.clicked.disconnect()
    widget.playButton.clicked.connect(lambda: pause(widget, player))
    widget.set_pause_icon_for_play_button()
    widget.set_pause_tooltip_for_the_play_button()
    player.play()


def pause(widget, player):
    widget.playButton.clicked.disconnect()
    widget.playButton.clicked.connect(lambda: play(widget, player))
    widget.set_play_icon_for_play_button()
    widget.set_play_tooltip_for_the_play_button()
    player.pause()


def stop(widget, player):
    widget.playButton.clicked.disconnect()
    widget.playButton.clicked.connect(lambda: play(widget, player))
    widget.set_play_icon_for_play_button()
    widget.set_play_tooltip_for_the_play_button()
    player.stop()
    # Открывает окно для выбора радиостанции
    widget.select_station_form(lambda: change_radio_station(widget, player))


def mute_switch(widget, player):
    # Если звук выключен, включит звук и сменит иконку
    if player.is_mute():
        player.set_mute_state(False)
        widget.set_sound_on_icon_for_switch_button()
        widget.set_sound_off_tooltip_for_switch_button()
    else:
        player.set_mute_state(True)
        widget.set_sound_off_icon_for_switch_button()
        widget.set_sound_on_tooltip_for_switch_button()


def change_volume(widget, player):
    value = widget.get_position_volume_slider()
    
    if value in range(0, 101):
        player.set_volume(value)
    else:
        ui.show_warning('Внимание', 'Передано некорректное значение громкости!')


def set_radio_station_by_name(station_name, widget, player):
    station_url = utils.RADIO_STATIONS.get(station_name)

    if(station_url):
        player.pause()
        player.set_media(station_url)
        player.play()
        # Установка имени радиостанции в заголовок окна
        widget.set_title(station_name)
        widget.child.hide()
    else:
        ui.show_error('Критическая ошибка', 'Не удалось получить ссылку для станции %s' % station_name)


def change_radio_station(widget, player):
    station_name = widget.selected_station()

    set_radio_station_by_name(station_name, widget, player)


def prev_radio_station(widget, player):
    # Получение имени текущей радиостанции
    radio_station_name = widget.get_title()
    # Создание списка радиостанций для дальнейшего поиска в нём индекса текущей радиостанции
    radios_list = [name for name in utils.RADIO_STATIONS]

    try:
        # Поиск индекса текущей радиостанции
        index = radios_list.index(radio_station_name)
    except ValueError:
        # Если возникла ошибка поиска индекса радиостанции, установит значение индекса на 0
        index = 0

    if index == 0:
        # Если слушая первую радиостанцию нажать кнопку "Предыдущая радиостанция"
        # Список радиостанций начнется с конца
        index = len(radios_list)-1
    else:
        index -= 1

    station_name = radios_list[index]
    
    set_radio_station_by_name(station_name, widget, player)


def next_radio_station(widget, player):
    # Получение имени текущей радиостанции
    radio_station_name = widget.get_title()
    # Создание списка радиостанций для дальнейшего поиска в нём индекса текущей радиостанции 
    radios_list = [name for name in utils.RADIO_STATIONS]

    try:
        # Поиск индекса текущей радиостанции
        index = radios_list.index(radio_station_name)
    except ValueError:
        # Если возникла ошибка поиска индекса радиостанции, установит значение индекса на 0
        index = 0

    if index == len(radios_list)-1:
        # Если слушая последнюю радиостанцию нажать кнопку "Следующая радиостанция"
        # Список радиостанций начнется сначала
        index = 0
    else:
        index += 1

    station_name = radios_list[index]

    set_radio_station_by_name(station_name, widget, player)


def close_handler(widget, player):
    config = {}

    config['last_volume'] = widget.get_position_volume_slider()
    config['last_radio_station_name'] = widget.get_title()
    config['is_mute'] = player.is_mute()

    utils.save_config(config)


def main():
    # 
    os.chdir(os.path.dirname(sys.argv[0]))
    # 
    app = ui.QApplication(sys.argv)
    # Создание экземпляра класса графического интерфейса
    widget = ui.MainForm()
    # Загрузка конфигурации радио с прошлой сессии
    config = utils.load_config()
    # Создание экземпляра класса драйвера управления Vlc Media Player
    player = vlcplayerdriver.VlcPlayerDriver()
    # Установка последней радиостанции и установленой громкости
    radio_station_name = config.get('last_radio_station_name')
    # Получит url-адрес прошлой радиостанции, если по какой-то причине не удалось получить имя радиостанции, 
    # установит url-адрес XITFM.
    radio_station_url = utils.RADIO_STATIONS.get(radio_station_name, utils.RADIO_STATIONS.get('XITFM'))

    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]) and os.path.isfile(sys.argv[1]):
        # Установка имени радиостанции в заголовке окна радио
        widget.set_title(sys.argv[1])
        # Установка url адреса последней радиостанции
        player.set_media(sys.argv[1])

    elif radio_station_url is not None:
        # Установка имени радиостанции в заголовке окна радио
        widget.set_title(radio_station_name)
        # Установка url адреса последней радиостанции
        player.set_media(radio_station_url)
            

    # Установка громкости на уровень с прошлой сессии
    last_volume = config.get('last_volume')
    if last_volume is not None:
        # Установка прошлого значения громкости для радио
        player.set_volume(last_volume)
        # Установка позиции ползунка громкости на прошлое значение
        widget.set_position_volume_slider(last_volume)

    # Если в прошлом сеансе звук был отключен, вновь отключит звук
    is_mute = config.get('is_mute')
    if is_mute is True:
        # Устанавливаем иконку выключенного звука для кнопки отключения звука
        widget.set_sound_off_icon_for_switch_button()
        # Отключаем звук
        player.set_mute_state(True)
   
    # Плей/пауза
    widget.playButton.clicked.connect(lambda: play(widget, player))
    # Смена текущей радиостанции на предыдущую радиостанции
    widget.prevButton.clicked.connect(lambda: prev_radio_station(widget, player))
    # Остановка проигрывания
    widget.stopButton.clicked.connect(lambda: stop(widget, player))
    # Смена текущей радиостанции на следующую радиостанцию
    widget.nextButton.clicked.connect(lambda: next_radio_station(widget, player))
    # Выбор радиостанции
    widget.playlistButton.clicked.connect(
        lambda: widget.select_station_form(lambda: change_radio_station(widget, player)))
    # Включение/выключение звука
    widget.muteButton.clicked.connect(lambda: mute_switch(widget, player))
    # Регулировка громкости звука
    widget.volumeSlider.valueChanged.connect(lambda: change_volume(widget, player))
    # Установка функции сохраняющей конфигурацию при закрытии радио 
    widget.set_close_handler(lambda: close_handler(widget, player))

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
