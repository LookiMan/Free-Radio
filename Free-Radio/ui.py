import os
import sys
import ctypes

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


class BaseForm():
    """ Вынесены общие методы для всех форм """

    def _customize_window(self):
        # Установка высоты шапки окна
        header_height = 15
        # Убираем стандартную рамку
        self.Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # Установка иконки 
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join('images', 'icon.ico')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Form.setWindowIcon(icon)
        # 
        self.header = QLabel(self.Form)
        self.header.setGeometry(QtCore.QRect(0, 0, self.form_width, header_height))
        pixmap = QtGui.QPixmap(os.path.join('images', 'header.png'))
        self.header.setPixmap(pixmap)
        self.header.setObjectName('header')
        # Добавляем обработку событий нажатия отжатия клавиш мыши,
        # а также движения курсора для реализации перемещения окна радио
        self._setMoveEvents(self.header)

        self.closeHeaderButton = QPushButton(self.Form)
        self.closeHeaderButton.setGeometry(QtCore.QRect(self.form_width-20, 2, 11, 11))
        pixmap = QtGui.QIcon()
        pixmap.addPixmap(QtGui.QPixmap(os.path.join('images', 'close.png')), 
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closeHeaderButton.setIcon(pixmap)
        self.closeHeaderButton.setObjectName('close')
        self.closeHeaderButton.clicked.connect(self.closeEvent)
        self.closeHeaderButton.setFlat(True)
        self.closeHeaderButton.setToolTip('Закрыть')

        self.backgroundLabel = QLabel(self.Form)
        self.backgroundLabel.setGeometry(QtCore.QRect(0, 15, self.form_width, self.form_height-header_height))
        pixmap = QtGui.QPixmap(os.path.join('images', 'background.png'))
        pixmap_resized = pixmap.scaled(self.form_width, self.form_height-header_height)
        self.backgroundLabel.setPixmap(pixmap_resized)
        self.backgroundLabel.setObjectName('backgroundLabel')

        self.font = QtGui.QFont()
        self.font.setFamily('Segoe UI Semibold')
        self.font.setPointSize(8)
        self.font.setWeight(75)
        self.font.setBold(True)
       
        self.titleLabel = QLabel(self.Form)
        self.titleLabel.setFont(self.font)
        self.titleLabel.setGeometry(QtCore.QRect(10, 0, self.form_width-50, 15))
        self.titleLabel.setText('Заголовок')
        self.titleLabel.setObjectName('titleLabel')
        self._setMoveEvents(self.titleLabel)

   # 
    def _setMoveEvents(self, widget):
        win = widget.parentWidget().window()
        cursorShape = widget.cursor().shape()
        user32 = ctypes.windll.user32
        screensize = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
        moveSource = getattr(widget, 'mouseMoveEvent')
        pressSource = getattr(widget, 'mousePressEvent')
        releaseSource = getattr(widget, 'mouseReleaseEvent')
        
        # 
        def move(event):
            if(move.b_move):
                x = event.globalX() + move.x_korr - move.lastPoint.x()
                y = event.globalY() + move.y_korr - move.lastPoint.y()
                if x >= screensize[0] - win.geometry().width():
                    x = screensize[0] - win.geometry().width()
                if x <= 0:
                    x = 0
                if y >= screensize[1] - win.geometry().height():
                    y = screensize[1] - win.geometry().height()
                if y <= 0:
                    y = 0
                win.move(x, y)
                widget.setCursor(QtCore.Qt.SizeAllCursor)
            return moveSource(event)
        
        # 
        def press(event):
            if(event.button() == QtCore.Qt.LeftButton):
                x_korr = win.frameGeometry().x() - win.geometry().x()
                y_korr = win.frameGeometry().y() - win.geometry().y()
                parent = widget
                while not parent == win:
                    x_korr -= parent.x()
                    y_korr -= parent.y()
                    parent = parent.parent()

                move.__dict__.update({'lastPoint': event.pos(),  'b_move': True,  'x_korr': x_korr,  'y_korr': y_korr})
            else:
                move.__dict__.update({'b_move': False})
                widget.setCursor(cursorShape)
            return pressSource(event)

        # 
        def release(event):
            if(hasattr(move, 'x_korr') and hasattr(move, 'y_korr')):
                move.__dict__.update({'b_move': False})
                widget.setCursor(cursorShape)
                x = event.globalX() + move.x_korr - move.lastPoint.x()
                y = event.globalY() + move.y_korr - move.lastPoint.y()

                return releaseSource(event)


        setattr(widget, 'mouseMoveEvent', move)
        setattr(widget, 'mousePressEvent', press)
        setattr(widget, 'mouseReleaseEvent', release)
        move.__dict__.update({'b_move': False})

        return widget


    def closeEvent(self):
        """ 
        Базовый метод, вызывающийся при закрытии радио по нажатию на кастомный крестик.
        В классе MainForm этот метод переназначается.
        """
        self.close()


    def show(self):
        """ Отображение формы """
        self.Form.show()


    def hide(self):
        """ Скрытие формы """
        self.Form.hide()


    def minimize(self):
        """ Сворачивает окно """
        self.Form.showMinimized() 


    def close(self):
        """ Закрытие формы """

        # Если есть дочернее окно, закроет его
        if hasattr(self, 'child'):
            self.child.close()

        self.Form.close()


    def set_title(self, title):
        """ Метод для установки заголовка окна """
        self.titleLabel.setText(title)


    def get_title(self):
        """ Метод для получения заголовка окна """
        return self.titleLabel.text()


# 
class MainForm(BaseForm):
    def __init__(self):
        self.form_width = 384
        self.form_height = 60
        self.Form = QWidget()
        self.Form.setFixedSize(self.form_width, self.form_height)
        self.Form.setObjectName('Form')
        # Кастомизация базового окна
        self._customize_window()
        # Установка заголока окна
        self.set_title('Лучшее радио!')

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
       
        self.playButton = QPushButton(self.Form)
        self.playButton.setFont(self.font)
        play_icon = QtGui.QIcon()
        play_icon.addPixmap(QtGui.QPixmap(os.path.join('images', 'play.png')), 
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.playButton.setIcon(play_icon)
        self.playButton.setIconSize(QtCore.QSize(22, 22))
        self.playButton.setGeometry(QtCore.QRect(2, 20, 34, 32))
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
        self.prevButton.setGeometry(QtCore.QRect(38, 20, 34, 32))
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
        self.stopButton.setGeometry(QtCore.QRect(74, 20, 34, 32))
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
        self.nextButton.setGeometry(QtCore.QRect(110, 20, 34, 32))
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
        self.playlistButton.setGeometry(QtCore.QRect(152, 20, 34, 32))
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
        self.muteButton.setGeometry(QtCore.QRect(196, 20, 34, 32))
        self.muteButton.setObjectName('muteButton')
        self.muteButton.setFlat(True)
        self.muteButton.setToolTip('Выключить звук')

        self.volumeSlider = QSlider(self.Form)
        self.volumeSlider.setGeometry(QtCore.QRect(232, 25, 142, 22))
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setProperty('value', 60)
        self.volumeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.volumeSlider.setObjectName('volumeSlider')

        self._retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.Form)

    # 
    def _retranslateUi(self):
        self.Form.show()


    def closeEvent(self):
        """ Переназначение базового метода closeEvent класcа BaseForm """
        try:
            self._close_handler()
        except (PermissionError, TypeError):
            show_error('Возникла критическая ошибка', 
                'Не удалось сохранить текущую конфигурацию плейера')
            
            if show_question('Возникла критическая ошибка', 'Выйти без сохранения текущей конфигурации?'):
                self.close()
        else:
            self.close()

    #
    def _customize_window(self):
        """ Переназначение базового метода _customize_window класcа BaseForm """
        super()._customize_window()

        self.hideHeaderButton = QPushButton(self.Form)
        self.hideHeaderButton.setGeometry(QtCore.QRect(self.form_width-35, 2, 11, 11))
        pixmap = QtGui.QIcon()
        pixmap.addPixmap(QtGui.QPixmap(os.path.join('images', 'hide.png')), 
            QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.hideHeaderButton.setIcon(pixmap)
        self.hideHeaderButton.setObjectName('hide')
        self.hideHeaderButton.clicked.connect(self.minimize)
        self.hideHeaderButton.setFlat(True)
        self.hideHeaderButton.setToolTip('Свернуть')


    @property
    def child(self):
        return self.Form.child
     

    def set_close_handler(self, handler):
        self._close_handler = handler


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


    def select_station_form(self, callback):
        self.Form.SelectRadioStationForm.listenStatioButton.clicked.connect(callback)
        self.Form.SelectRadioStationForm.show()


    def selected_station(self):
        return self.Form.SelectRadioStationForm.get_selected_station()

# 
class SelectRadioStationForm(BaseForm):
    def __init__(self):
        self.form_width = 384
        self.form_height = 115
        self.Form = QWidget()
        self.Form.setFixedSize(self.form_width, self.form_height)
        self.Form.setObjectName('Form')
        self.Form.setEnabled(True)
        self.Form.setMouseTracking(False)
        self.Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # Кастомизация базового окна
        self._customize_window()
        # Установка заголока окна
        self.set_title('Выбор радиостанции')

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
        self.label.setGeometry(QtCore.QRect(10, 25, 181, 16))

        self.comboBox_1 = QComboBox(self.Form)
        self.comboBox_1.setObjectName(u"comboBox_1")
        self.comboBox_1.setGeometry(QtCore.QRect(10, 50, 366, 22))
        # Добавляет радиостанции в выпадающий список 
        self.update_combobox(utils.RADIO_STATIONS)

        self.appendStationButton = QPushButton(self.Form)
        self.appendStationButton.setFont(self.font)
        self.appendStationButton.setGeometry(QtCore.QRect(10, 75, 142, 32))
        self.appendStationButton.setObjectName('appendStationButton')
        self.appendStationButton.setFlat(True)
        self.appendStationButton.clicked.connect(self.append_station_window_show)

        self.deleteStatioButton = QPushButton(self.Form)
        self.deleteStatioButton.setFont(self.font)
        self.deleteStatioButton.setGeometry(QtCore.QRect(255, 75, 63, 32))
        self.deleteStatioButton.setObjectName('deleteStatioButton')
        self.deleteStatioButton.setFlat(True)
        self.deleteStatioButton.clicked.connect(self.delete_station)

        self.listenStatioButton = QPushButton(self.Form)
        self.listenStatioButton.setFont(self.font)
        self.listenStatioButton.setGeometry(QtCore.QRect(315, 75, 63, 32))
        self.listenStatioButton.setObjectName('listenStatioButton')
        self.listenStatioButton.setFlat(True)
        self.listenStatioButton.clicked.connect(self.get_selected_station)

        self._retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.Form)

    # 
    def _retranslateUi(self):
        self.appendStationButton.setText(QApplication.translate('Form', 'Добавить радиостанцию', None))
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
        self.form_width = 384
        self.form_height = 135
        self.Form = QWidget()
        self.Form.setFixedSize(self.form_width, self.form_height)
        self.Form.setObjectName('Form')
        self.Form.setEnabled(True)
        self.Form.setMouseTracking(False)
        self.Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # Кастомизация базового окна
        self._customize_window()
        # Установка заголока окна
        self.set_title('Добавление новой радиостанции')

        self._callback = None

        self.font = QtGui.QFont()
        self.font.setFamily('Segoe UI Semibold')
        self.font.setPointSize(8)
        self.font.setWeight(75)
        self.font.setBold(True)

        self.label = QLabel(self.Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QtCore.QRect(10, 25, 366, 16))

        self.nameLineEdit = QLineEdit(self.Form)
        self.nameLineEdit.setObjectName(u"nameLineEdit")
        self.nameLineEdit.setGeometry(QtCore.QRect(10, 50, 366, 21))
        self.nameLineEdit.setPlaceholderText('Имя радиостанции')

        self.urlLineEdit = QLineEdit(self.Form)
        self.urlLineEdit.setObjectName(u"urlLineEdit")
        self.urlLineEdit.setGeometry(QtCore.QRect(10, 75, 366, 21))
        self.urlLineEdit.setPlaceholderText('URL адрес')

        self.closeButton = QPushButton(self.Form)
        self.closeButton.setFont(self.font)
        self.closeButton.setGeometry(QtCore.QRect(250, 100, 63, 32))
        self.closeButton.setObjectName('pushButton_2')
        self.closeButton.setFlat(True)
        self.closeButton.clicked.connect(self.clearn_fields_and_hide)

        self.addButton = QPushButton(self.Form)
        self.addButton.setFont(self.font)
        self.addButton.setGeometry(QtCore.QRect(315, 100, 63, 32))
        self.addButton.setObjectName('addButton')
        self.addButton.setFlat(True)
        self.addButton.clicked.connect(self.append_station)

        self._retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.Form)

    # 
    def _retranslateUi(self):
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

