import sys
import os

import vlcplayerdriver
import ui
import utils



class Engine:
    """ Класс связующий между собой графический интерфейс и драйвер плеера """
    def __init__(self, ui, player):
        self.ui = ui
        self.player = player


    def play(self):
        """ Начало воспроизведения аудио """
        self.ui.hide_play_button()
        self.ui.show_pause_button()
        self.player.play()


    def pause(self):
        """ Остановка воспроизведения аудио """
        self.ui.hide_pause_button()
        self.ui.show_play_button()
        self.player.pause()


    def change_volume(self, value):
        """ Смена громкости воспроизведения аудио """
        if value in range(0, 101):
            self.player.set_volume(value)
        else:
            ui.show_warning('Внимание', 'Передано некорректное значение громкости!')


    def set_title(self, title):
        """ Установка заголовка приложения """
        self.ui.set_title(title)


    def set_media(self, media):
        """ Установка url-адреса для воспроизведения аудио """
        self.player.set_media(media)


    def set_volume(self, volume):
        """ Установка значения громкости для плеера при запуске радио """
        self.player.set_volume(volume)
        self.ui.set_position_volume_slider(volume)


    def set_radio_station_by_name(self, station_name):
        """ Установка радиостанции по ее имени """
        station_url = utils.RADIO_STATIONS.get(station_name)

        if(station_url):
            self.player.pause()
            self.player.set_media(station_url)
            self.player.play()
            # Установка имени радиостанции в заголовок окна
            self.ui.set_title(station_name)
        else:
            ui.show_error('Критическая ошибка', 'Не удалось получить ссылку для станции %s' % station_name)


    def get_radio_stations_list(self):
        """ Создание списка радиостанций для дальнейшего поиска в нём индекса текущей радиостанции"""
        return [name for name in utils.RADIO_STATIONS]       


    def get_station_index(self):
        """ Получение индекса текущей радиостанции """
        radio_station_name = self.ui.get_title()
        radios_list = self.get_radio_stations_list()

        try:
            # Поиск индекса текущей радиостанции
            index = radios_list.index(radio_station_name)
        except ValueError:
            # Если возникла ошибка поиска индекса радиостанции, установит значение индекса на 0
            index = 0

        return index


    def prev_radio_station(self):
        """ Переключение на предыдущую радиостанцию """
        index = self.get_station_index()
        radios_list = self.get_radio_stations_list()
        
        if index == 0:
            # Если, слушая первую радиостанцию нажать кнопку "Предыдущая радиостанция"
            # Список радиостанций начнется с конца
            index = len(radios_list)-1
        else:
            index -= 1

        station_name = radios_list[index]
        
        self.set_radio_station_by_name(station_name)


    def next_radio_station(self):
        """ Переключение на следующую радиостанцию """
        index = self.get_station_index()
        radios_list = self.get_radio_stations_list()

        if index == len(radios_list)-1:
            # Если, слушая последнюю радиостанцию нажать кнопку "Следующая радиостанция"
            # Список радиостанций начнется сначала
            index = 0
        else:
            index += 1

        station_name = radios_list[index]

        self.set_radio_station_by_name(station_name)


def main():
    app = ui.QApplication(sys.argv)
    # Создание экземпляра класса графического интерфейса
    widget = ui.MainForm()
    # Загрузка конфигурации радио с прошлой сессии
    config = utils.load_config()
    # Создание экземпляра класса драйвера управления Vlc Media Player
    try:
        player = vlcplayerdriver.VlcPlayerDriver()
    except:
        # Может возникнуть только VLCException
        ui.show_error('Критическая ошибка', 
            'Возникла непредвиденная ошибка с VLC media player')
    # Установка последней радиостанции и установленной громкости
    radio_station_name = config.get('last_radio_station_name')
    # Получит url-адрес прошлой радиостанции, если по какой-то причине не удалось получить имя радиостанции, 
    # установит url-адрес XITFM.
    radio_station_url = utils.RADIO_STATIONS.get(radio_station_name, 
        utils.RADIO_STATIONS.get('XITFM'))
    # Инициализация движка связующего графический интерфейс с драйвером плеера
    engine = Engine(widget, player)

    if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
        # Установка имени радиостанции в заголовке окна радио
        engine.set_title(sys.argv[1])
        # Установка url адреса последней радиостанции
        engine.set_media(sys.argv[1])

    elif radio_station_url is not None:
        # Установка имени радиостанции в заголовке окна радио
        engine.set_title(radio_station_name)
        # Установка url адреса последней радиостанции
        engine.set_media(radio_station_url)
    
    # Установка громкости на уровень с прошлой сессии
    last_volume = config.get('last_volume')
    if last_volume is not None:
        # Установка прошлого значения громкости для радио
        engine.set_volume(last_volume)

    # Плей
    widget.playButton.clicked.connect(engine.play)
    # Пауза
    widget.pauseButton.clicked.connect(engine.pause)
    # Смена текущей радиостанции на предыдущую радиостанции
    widget.prevButton.clicked.connect(engine.prev_radio_station)
    # Смена текущей радиостанции на следующую радиостанцию
    widget.nextButton.clicked.connect(engine.next_radio_station)
    # Регулировка громкости звука
    widget.volumeSlider.valueChanged.connect(engine.change_volume)
    # Привязка функции смены радиостанции для формы SelectRadioStationForm
    widget.child_form.callback.connect(engine.set_radio_station_by_name)
    # Установка функции сохраняющей конфигурацию при закрытии радио
    widget.closeHandler.connect(utils.save_config)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
