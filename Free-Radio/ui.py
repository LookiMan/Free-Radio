import os
import sys

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QPushButton, QMessageBox, QLabel, QSlider, QComboBox, QLineEdit
from PyQt5 import QtCore, QtGui

import utils


# 
def show_info(title: str, message_text: str):
    QMessageBox.information(None, title, message_text, QMessageBox.Ok)

# 
def show_warning(title: str, message_text: str):
    QMessageBox.warning(None, title, message_text, QMessageBox.Ok)

# 
def show_error(title: str, message_text: str):
    QMessageBox.critical(None, title, message_text, QMessageBox.Ok)

# 
def show_question(title: str, message_text: str):
    result = QMessageBox.question(None, title, message_text, QMessageBox.Yes, QMessageBox.No)
    if(result == 16384):
        return True
    elif(result == 65536):
        return False


class CustomWidget(QWidget):
    """  """
    # Переназначение метода closeEvent 
    def closeEvent(self, event):
        try:
            self._close_handler()
        except (PermissionError, TypeError):
            show_error('Возникла критическая ошибка', 
                'Не удалось сохранить текущую конфигурацию плейера')
            
            if show_question('Возникла критическая ошибка', 
                'Выйти без сохранения текущей конфигурации?'):
                event.accept()
            else:
                event.ignore()
        else:
            # Если есть дочернее окно, закроет его
            if hasattr(self, 'child'):
                self.child.close()

            event.accept()


class BaseForm():
    """ Вынесены общие методы для всех форм """

    def show(self):
        """ Отображение формы """
        self.Form.show()


    def hide(self):
        """ Скрытие формы """
        self.Form.hide()


    def close(self):
        """ Закрытие формы """

        # Если есть дочернее окно, закроет его
        if hasattr(self, 'child'):
            self.child.close()

        self.Form.close()

# 
class MainForm(BaseForm):
    def __init__(self):
        self.Form = CustomWidget()
        self.Form.setFixedSize(400, 50)
        self.Form.setObjectName('Form')
        self.Form.setEnabled(True)
        self.Form.setMouseTracking(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join('images', 'icon.ico')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Form.setWindowIcon(icon)

        self.Form.SelectRadioStationForm = SelectRadioStationForm()
        # Привязка поля Form.SelectRadioStationForm к полю Form.child для корректной работы метода close 
        # обвяленного в классе BaseForm
        self.Form.child = self.Form.SelectRadioStationForm 
        self._close_handler = None

        self.font = QtGui.QFont()
        self.font.setFamily('Segoe UI Semibold')
        self.font.setPointSize(8)
        self.font.setWeight(75)
        self.font.setBold(True)

        self.label = QLabel(self.Form)
        self.label.setGeometry(QtCore.QRect(0, 0, 500, 50))
        pixmap = QtGui.QPixmap(os.path.join('images', 'background.png'))
        pixmap_resized = pixmap.scaled(500, 50)
        self.label.setPixmap(pixmap_resized)
        self.label.setObjectName('label')
       
        self.playButton = QPushButton(self.Form)
        self.playButton.setFont(self.font)
        play_icon = QtGui.QIcon()
        play_icon.addPixmap(QtGui.QPixmap(os.path.join('images', 'play.png')), 
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.playButton.setIcon(play_icon)
        self.playButton.setIconSize(QtCore.QSize(22, 22))
        self.playButton.setGeometry(QtCore.QRect(10, 10, 34, 32))
        self.playButton.setObjectName('playButton')
        self.playButton.setFlat(True)
        self.playButton.setToolTip('Играть')

        self.prevButton = QPushButton(self.Form)
        self.prevButton.setFont(self.font)
        stop_icon = QtGui.QIcon()
        stop_icon.addPixmap(QtGui.QPixmap(os.path.join('images', 'prev.png')), 
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.prevButton.setIcon(stop_icon)
        self.prevButton.setIconSize(QtCore.QSize(22, 22))
        self.prevButton.setGeometry(QtCore.QRect(46, 10, 34, 32))
        self.prevButton.setObjectName('prevButton')
        self.prevButton.setFlat(True)
        self.prevButton.setToolTip('Предыдущая радиостанция')

        self.stopButton = QPushButton(self.Form)
        self.stopButton.setFont(self.font)
        stop_icon = QtGui.QIcon()
        stop_icon.addPixmap(QtGui.QPixmap(os.path.join('images', 'stop.png')), 
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stopButton.setIcon(stop_icon)
        self.stopButton.setIconSize(QtCore.QSize(22, 22))
        self.stopButton.setGeometry(QtCore.QRect(82, 10, 34, 32))
        self.stopButton.setObjectName('stopButton')
        self.stopButton.setFlat(True)
        self.stopButton.setToolTip('Стоп')

        self.nextButton = QPushButton(self.Form)
        self.nextButton.setFont(self.font)
        stop_icon = QtGui.QIcon()
        stop_icon.addPixmap(QtGui.QPixmap(os.path.join('images', 'next.png')), 
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.nextButton.setIcon(stop_icon)
        self.nextButton.setIconSize(QtCore.QSize(22, 22))
        self.nextButton.setGeometry(QtCore.QRect(118, 10, 34, 32))
        self.nextButton.setObjectName('nextButton')
        self.nextButton.setFlat(True)
        self.nextButton.setToolTip('Следующая радиостанция')
  
        self.playlistButton = QPushButton(self.Form)
        self.playlistButton.setFont(self.font)
        playlist_icon = QtGui.QIcon()
        playlist_icon.addPixmap(QtGui.QPixmap(os.path.join('images', 'playlist.png')), 
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.playlistButton.setIcon(playlist_icon)
        self.playlistButton.setIconSize(QtCore.QSize(22, 22))
        self.playlistButton.setGeometry(QtCore.QRect(160, 10, 34, 32))
        self.playlistButton.setObjectName('playlistButton')
        self.playlistButton.setFlat(True)
        self.playlistButton.setToolTip('Список радиостанций')

        self.muteButton = QPushButton(self.Form)
        self.muteButton.setFont(self.font)
        sound_icon = QtGui.QIcon()
        sound_icon.addPixmap(QtGui.QPixmap(os.path.join('images', 'sound-on.png')), 
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.muteButton.setIcon(sound_icon)
        self.muteButton.setIconSize(QtCore.QSize(24, 24))
        self.muteButton.setGeometry(QtCore.QRect(202, 10, 34, 32))
        self.muteButton.setObjectName('muteButton')
        self.muteButton.setFlat(True)
        self.muteButton.setToolTip('Выключить звук')

        self.volumeSlider = QSlider(self.Form)
        self.volumeSlider.setGeometry(QtCore.QRect(240, 15, 142, 22))
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setProperty('value', 60)
        self.volumeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.volumeSlider.setObjectName('volumeSlider')

        self._retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.Form)

    # 
    def _retranslateUi(self):
        self.Form.setWindowTitle(QApplication.translate('Form', 'Лучшее радио!', None))
        self.Form.show()


    @property
    def child(self):
        return self.Form.child
     

    def set_close_handler(self, handler):
        self.Form._close_handler = handler


    def set_title(self, title):
        self.Form.setWindowTitle(QApplication.translate('Form', title, None))       


    def set_play_icon_for_play_button(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join('images', 'play.png')), 
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.playButton.setIcon(icon)


    def set_play_tooltip_for_the_play_button(self):
        self.playButton.setToolTip('Играть')


    def set_pause_icon_for_play_button(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join('images', 'pause.png')), 
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.playButton.setIcon(icon)


    def set_pause_tooltip_for_the_play_button(self):
        self.playButton.setToolTip('Пауза')


    def set_sound_off_icon_for_switch_button(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join('images', 'sound-off.png')), 
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.muteButton.setIcon(icon)


    def set_sound_off_tooltip_for_switch_button(self):
        self.muteButton.setToolTip('Выключить звук')


    def set_sound_on_icon_for_switch_button(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join('images', 'sound-on.png')), 
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.muteButton.setIcon(icon)


    def set_sound_on_tooltip_for_switch_button(self):
        self.muteButton.setToolTip('Включить звук')


    def set_position_volume_slider(self, value):
        return self.volumeSlider.setProperty('value', value)


    def get_position_volume_slider(self):
        return self.volumeSlider.value()


    def get_title(self):
        return self.Form.windowTitle()


    def select_station_form(self, callback):
        self.Form.SelectRadioStationForm.listenStatioButton.clicked.connect(callback)
        self.Form.SelectRadioStationForm.show()


    def selected_station(self):
        return self.Form.SelectRadioStationForm.get_selected_station()

# 
class SelectRadioStationForm(BaseForm):
    def __init__(self):
        self.Form = QWidget()
        self.Form.setFixedSize(400, 100)
        self.Form.setObjectName('Form')
        self.Form.setEnabled(True)
        self.Form.setMouseTracking(False)
        self.AppendStationForm = AppendStationForm()
        # Привязка поля AppendStationForm к полю child для корректной работы метода close 
        # обвяленного в классе BaseForm
        self.child = self.AppendStationForm

        self.font = QtGui.QFont()
        self.font.setFamily('Segoe UI Semibold')
        self.font.setPointSize(8)
        self.font.setWeight(75)
        self.font.setBold(True)

        self.label = QLabel(self.Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QtCore.QRect(10, 10, 181, 16))

        self.comboBox_1 = QComboBox(self.Form)
        self.comboBox_1.setObjectName(u"comboBox_1")
        self.comboBox_1.setGeometry(QtCore.QRect(10, 30, 380, 22))
        # Добавляет радиостанции в выпадающий список 
        self.update_combobox(utils.RADIO_STATIONS)

        self.appendStationButton = QPushButton(self.Form)
        self.appendStationButton.setFont(self.font)
        self.appendStationButton.setGeometry(QtCore.QRect(10, 60, 185, 32))
        self.appendStationButton.setObjectName('appendStationButton')
        self.appendStationButton.clicked.connect(self.append_station_window_show)

        self.closeFormButton = QPushButton(self.Form)
        self.closeFormButton.setFont(self.font)
        self.closeFormButton.setGeometry(QtCore.QRect(198, 60, 62, 32))
        self.closeFormButton.setObjectName('closeFormButton')
        self.closeFormButton.clicked.connect(self.hide)

        self.deleteStatioButton = QPushButton(self.Form)
        self.deleteStatioButton.setFont(self.font)
        self.deleteStatioButton.setGeometry(QtCore.QRect(263, 60, 63, 32))
        self.deleteStatioButton.setObjectName('deleteStatioButton')
        self.deleteStatioButton.clicked.connect(self.delete_station)

        self.listenStatioButton = QPushButton(self.Form)
        self.listenStatioButton.setFont(self.font)
        self.listenStatioButton.setGeometry(QtCore.QRect(328, 60, 63, 32))
        self.listenStatioButton.setObjectName('listenStatioButton')
        self.listenStatioButton.clicked.connect(self.get_selected_station)

        self._retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.Form)

    # 
    def _retranslateUi(self):
        self.Form.setWindowTitle(QApplication.translate('Form', 'Выбор радиостанции', None))
        self.appendStationButton.setText(QApplication.translate('Form', 'Добавить радиостанцию', None))
        self.closeFormButton.setText(QApplication.translate('Form', 'Отмена', None))
        self.deleteStatioButton.setText(QApplication.translate('Form', 'Удалить', None))
        self.listenStatioButton.setText(QApplication.translate('Form', 'Слушать', None))
        self.label.setText(QApplication.translate('Form', 'Все радиостанции', None))


    def update_combobox(self, lst: dict):
        """ Обновление списка радиостанций """
        self.comboBox_1.clear()
        for stations in lst:
            self.comboBox_1.addItem(stations)


    def append_station(self, radio_name, radio_url):
        # Добавление имени и адреса радиостанции в глобальный словарь модуля utils
        utils.append_new_radio_station(radio_name, radio_url)
        # Обновление списка радиостанций
        self.update_combobox(utils.RADIO_STATIONS)


    def delete_station(self):
        """ Удаление радиостанции """
        radio_station_name = self.get_selected_station()

        if show_question('Внимание', 'Вы действительно ходите удалить радиостанцию "%s"?' % radio_station_name):
            try:
                # Добавление имени и адреса радиостанции в глобального словаря модуля utils
                utils.delete_radio_station(radio_station_name)
            except KeyError:
                show_error('Критическая ошибка', 'Радиостация %s не найдена!')
            except:
                show_error('Критическая ошибка', 'Возникла непредвиденая ошибка!')
            else:
                # Обновление списка радиостанций
                self.update_combobox(utils.RADIO_STATIONS)


    def append_station_window_show(self):
        """ Отображает форму добавления радиостанции """
        self.AppendStationForm._callback = self.append_station
        self.AppendStationForm.show()


    def get_selected_station(self):
        """ Возвращает выбранную радиостанцию """
        return self.comboBox_1.currentText()


class AppendStationForm(BaseForm):
    def __init__(self):
        self.Form = QWidget()
        self.Form.setFixedSize(400, 125)
        self.Form.setObjectName('Form')
        self.Form.setEnabled(True)
        self.Form.setMouseTracking(False)
        self._callback = None

        self.font = QtGui.QFont()
        self.font.setFamily('Segoe UI Semibold')
        self.font.setPointSize(8)
        self.font.setWeight(75)
        self.font.setBold(True)
        self.label = QLabel(self.Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QtCore.QRect(10, 10, 281, 16))

        self.nameLineEdit = QLineEdit(self.Form)
        self.nameLineEdit.setObjectName(u"nameLineEdit")
        self.nameLineEdit.setGeometry(QtCore.QRect(10, 35, 380, 21))
        self.nameLineEdit.setPlaceholderText('Имя радиостанции')

        self.urlLineEdit = QLineEdit(self.Form)
        self.urlLineEdit.setObjectName(u"urlLineEdit")
        self.urlLineEdit.setGeometry(QtCore.QRect(10, 60, 380, 21))
        self.urlLineEdit.setPlaceholderText('URL адрес')

        self.addButton = QPushButton(self.Form)
        self.addButton.setFont(self.font)
        self.addButton.setGeometry(QtCore.QRect(298, 85, 92, 32))
        self.addButton.setObjectName('addButton')
        self.addButton.clicked.connect(self.append_station)

        self.closeButton = QPushButton(self.Form)
        self.closeButton.setFont(self.font)
        self.closeButton.setGeometry(QtCore.QRect(203, 85, 93, 32))
        self.closeButton.setObjectName('pushButton_2')
        self.closeButton.clicked.connect(self.clearn_fields_and_hide)

        self._retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.Form)

    # 
    def _retranslateUi(self):
        self.Form.setWindowTitle(QApplication.translate('Form', 'Добавление новой радиостанции', None))
        self.label.setText(QApplication.translate('Form', 'Введите имя и url-адрес новой радиостанции', None))
        self.addButton.setText(QApplication.translate('Form', 'Добавить', None))
        self.closeButton.setText(QApplication.translate('Form', 'Отмена', None))


    def _get_radio_station_name(self):
        """ Получение имени радиостанции с поля namelineEdit """
        return self.nameLineEdit.text()


    def _get_radio_station_url(self):
        """ Получение url-адреса радиостанции с поля urllineEdit """
        return self.urlLineEdit.text()


    def _clearn_radio_station_name_field(self):
        """ Очистка поля 'имя радиостанции' """
        self.nameLineEdit.setText('')


    def _clearn_radio_station_url_field(self):
        """ Очистка поля 'URL адрес' """
        self.urlLineEdit.setText('')


    def _clearn_all_fields(self):
        """ Очистка полей 'имя радиостанции' и 'URL адрес' """
        self._clearn_radio_station_name_field()
        self._clearn_radio_station_url_field()


    def append_station(self):
        """ Добавление новой радиостанции """
        radio_station_name = self._get_radio_station_name()
        radio_station_url = self._get_radio_station_url()

        if radio_station_name == '':
            show_warning('Внимание', 'Укажите имя радиостанции')

        elif radio_station_url == '':
            show_warning('Внимание', 'Укажите url-адрес радиостанции')

        else:
            self._callback(radio_station_name, radio_station_url)
            self._clearn_all_fields()
            self.hide()


    def clearn_fields_and_hide(self):
        """ Скрытие формы добавления радиостанции с очисткой полей """
        self._clearn_all_fields()
        self.hide()

