import os
import sys

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QPushButton, QMessageBox, QLabel, QGroupBox, QComboBox, QLineEdit
from PyQt5 import QtCore, QtGui

import utils


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


class ClickedQLabel(QLabel):
    """ Класс добавляющий событие клика базовому классу QLabel """
    clicked = QtCore.pyqtSignal()

    def mouseReleaseEvent(self, event):
        self.clicked.emit()
        super().mouseReleaseEvent(event)


class BaseMoveEvents(QWidget):
    """ Реализация базовых методов для шапки приложения """
    def _get_window(self):
        return self._parent.window()


    def _get_window_width(self):
        return self._parent.window().geometry().width()


    def _get_window_height(self):
        return self._parent.window().geometry().height()


    def _get_screen_size(self):
        return (utils.get_screen_width(), utils.get_screen_height())


    def mouseMoveEvent(self, event):
        win = self._get_window()
        screensize = self._get_screen_size()

        if(self.b_move):
            x = event.globalX() + self.x_korr - self.lastPoint.x()
            y = event.globalY() + self.y_korr - self.lastPoint.y()
            if x >= screensize[0] - self._get_window_width():
                x = screensize[0] - self._get_window_width()
            if x <= 0:
                x = 0
            if y >= screensize[1] - self._get_window_height():
                y = screensize[1] - self._get_window_height()
            if y <= 0:
                y = 0
            win.move(x, y)
            
        super().mouseMoveEvent(event)


    def mousePressEvent(self, event):
        if(event.button() == QtCore.Qt.LeftButton):
            win = self._get_window()
            x_korr = win.frameGeometry().x() - win.geometry().x()
            y_korr = win.frameGeometry().y() - win.geometry().y()
            parent = self
            while not parent == win:
                x_korr -= parent.x()
                y_korr -= parent.y()
                parent = parent.parent()

            self.__dict__.update({'lastPoint': event.pos(),  'b_move': True,  'x_korr': x_korr,  'y_korr': y_korr})
        else:
            self.__dict__.update({'b_move': False})

        self.setCursor(QtCore.Qt.SizeAllCursor)
        super().mousePressEvent(event)


    def mouseReleaseEvent(self, event):
        if(hasattr(self, 'x_korr') and hasattr(self, 'y_korr')):
            self.__dict__.update({'b_move': False})
            x = event.globalX() + self.x_korr - self.lastPoint.x()
            y = event.globalY() + self.y_korr - self.lastPoint.y()

        self.setCursor(QtCore.Qt.ArrowCursor) 
        super().mouseReleaseEvent(event)


class Panel(QLabel, BaseMoveEvents):
    """ Панель заголовка окна приложения """
    def __init__(self, parent, width: int, height: int):
        super(QLabel, self).__init__(parent)
        self._parent = parent 
        self._width = width
        self._height = height
        self.setGeometry(QtCore.QRect(0, 0, self._width, self._height))
        self._pixmap = QtGui.QPixmap('images\\header.png')
        self.setScaledContents(True)
        self.setPixmap(self._pixmap)
        self.setObjectName('header')


class Title(QLabel, BaseMoveEvents):
    """ Заголовок окна приложения """
    def __init__(self, parent, width: int, height: int):
        super(QLabel, self).__init__(parent)
        self._parent = parent 
        self._width = width
        self._height = height
        self.font = QtGui.QFont()
        self.font.setFamily('Segoe UI Semibold')
        self.font.setPointSize(8)
        self.font.setWeight(75)
        self.font.setBold(True)
        self.setStyleSheet('color: rgb(255,255,255);')
        self.setFont(self.font)
        self.setGeometry(QtCore.QRect(10, 0, self._width, self._height))
        self.setText('Заголовок')
        self.setObjectName('titleLabel')


    def set_title(self, title):
        self.setText(title)


    def get_title(self):
        return self.text()


class BaseButtonEvents(QWidget):
    """ Общие методы для реализации ховер еффекта """
    def enterEvent(self, event):
        self.setPixmap(self.pixmap_enter)
        super().enterEvent(event)


    def leaveEvent(self, event):
        self.setPixmap(self.pixmap_leave)
        super().leaveEvent(event)


class HideButton(ClickedQLabel, BaseButtonEvents):
    """ Кнопка сворачивания приложения """
    def __init__(self, parent, x, y, size=26):
        super(QLabel, self).__init__(parent)
        self.pixmap = QtGui.QPixmap('images/hide.png')
        self.pixmap_leave = self.pixmap.copy(0, 0, size, size)
        self.pixmap_enter = self.pixmap.copy(size, 0, size*2, size)
        
        self.setGeometry(QtCore.QRect(x, y, size, size))
        self.setPixmap(self.pixmap_leave)
        self.setObjectName('minimize_button')
        self.setToolTip('Свернуть')


class CloseButton(ClickedQLabel, BaseButtonEvents):
    """ Кнопка закрытия приложения """
    def __init__(self, parent, x, y, size=26):
        super(QLabel, self).__init__(parent)
        self.pixmap = QtGui.QPixmap('images/close.png')
        self.pixmap_leave = self.pixmap.copy(0, 0, size, size)
        self.pixmap_enter = self.pixmap.copy(size, 0, size*2, size)
        
        self.setGeometry(QtCore.QRect(x, y, size, size))
        self.setPixmap(self.pixmap_leave)
        self.setObjectName('close_button')
        self.setToolTip('Закрыть')


class Header:
    """ Шапка приложения с заголовком и кнопками закрытия и сворачивания """
    def __init__(self, parent):
        self._height = 26
        self.panel = Panel(parent, parent.width(), self._height)
        self.title = Title(parent, parent.width()*0.8, self._height)
        self.hide_button = HideButton(parent, parent.width()-self._height*2, 0, self._height)
        self.close_button = CloseButton(parent, parent.width()-self._height, 0, self._height)


    def width(self):
        return self._width


    def height(self):
        return self._height


class Background:
    """ Задний фон приложения """
    def __init__(self, parent, path):
        self._parent = parent
        # Белый фон с черными рамками
        self._background = QLabel(self._parent)
        self._background.setScaledContents(True)
        self._background.setGeometry(QtCore.QRect(0, 0, self._parent.width(), self._parent.height()))
        pixmap = QtGui.QPixmap(path)
        pixmap_resized = pixmap.scaled(self._parent.width(), self._parent.height())
        self._background.setPixmap(pixmap_resized)
        self._background.setObjectName('background')
        self._background_image = None


    def set_image(self, path):   
        """ Установка изображения на задний фон """
        self._background_image = QLabel(self._parent)
        self._background_image.setGeometry(QtCore.QRect(1, 0, self._parent.width()-2, self._parent.height()-1))
        pixmap = QtGui.QPixmap(path)
        pixmap_resized = pixmap.scaled(self._parent.width()-2, self._parent.height()-1)
        self._background_image.setPixmap(pixmap_resized)
        self._background_image.setObjectName('background_image')        
        self._background_image.show()


class BaseForm(QtCore.QObject):
    closeHandler = QtCore.pyqtSignal(dict)
    """ Вынесены общие методы для всех форм """    
    def _customize_window(self):
        """ Создание кастомного окна """
        
        # Убираем стандартную рамку
        self.form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # Установка иконки 
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('images/icon.ico'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.form.setWindowIcon(icon)

        self.background = Background(self.form, 'images\\background.png')
        self.background.set_image('images\\background_image')

        self.header = Header(self.form)
        self.header.hide_button.clicked.connect(self.minimize)
        self.header.close_button.clicked.connect(self.closeEvent)


    def closeEvent(self):
        """ 
        Базовый метод, вызывающийся при закрытии по нажатию на кастомный крестик.
        """
        self.close()


    def show(self):
        """ Отображение формы """
        self.form.show()


    def hide(self):
        """ Скрытие формы """
        self.form.hide()


    def minimize(self):
        """ Сворачивает окно """
        self.form.showMinimized() 


    def close(self):
        """ Закрытие формы """

        # Если есть дочернее окно, закроет его
        if hasattr(self, 'child_form'):
            self.child_form.close()

        self.form.close()


    def set_title(self, title):
        """ Метод для установки заголовка окна """
        self.header.title.set_title(title)


    def get_title(self):
        """ Метод для получения заголовка окна """
        return self.header.title.get_title()


    def set_background_image(self, path):
        """ Установка изображения на задний фон """
        self.background.set_image(path)


class CustomSlider(QWidget):
    valueChanged = QtCore.pyqtSignal(int)
    """ Кастомный слайдер """
    def __init__(self, parent, x, y, width=200):
        super().__init__()
        self.parent = parent
        self.x = x
        self.y = y
        self.width = width

        self.slider_position = 0
        self.min_value = 0
        self.max_value = 10

        self.height = 4
        self.slider_radius = 16

        self.image = QtGui.QPixmap('images/slider.png')

        self._background_line = self._make_background_line()
        self._foreground_line = self._make_foreground_line()
        self._slider = self._make_slider()

        self.setValue(self.slider_position)


    def _get_parent_window_x(self):
        return self.parent.window().geometry().x()


    def _get_slider_width(self):
        return self.width-self.slider_radius

    
    def _get_slider_position(self):
        return self.slider_position-self.x


    def _get_slider_y(self):
        return self.y-(self.slider_radius/2)+self.height/2


    def _get_slider_min_position(self):
        return self.x


    def _get_slider_max_position(self):
        return self._get_slider_min_position()+self._get_slider_width()


    def _make_background_line(self):
        background_line = QLabel(self.parent)
        background_line.setObjectName('background_line')
        background_line.setGeometry(QtCore.QRect(self.x, self.y, self.width, self.height))
        background_line.setScaledContents(True)
        background_line.setPixmap(self.image.copy(0, 2, 316, 4))

        return background_line
 

    def _make_foreground_line(self): 
        foreground_line = QLabel(self.parent)
        foreground_line.setObjectName('foreground_line')
        foreground_line.setScaledContents(True)
        foreground_line.setPixmap(self.image.copy(0, 6, 316, 4))
        foreground_line.setGeometry(QtCore.QRect(self.x, self.y, self.slider_position, self.height))

        return foreground_line

     
    def _make_slider(self):
        slider = QLabel(self.parent)
        slider.setObjectName('slider')
        slider.setGeometry(QtCore.QRect(self.x, self._get_slider_y(), self.slider_radius, self.slider_radius))
        slider.setScaledContents(True)
        slider.setPixmap(self.image.copy(316, 0, self.slider_radius, self.slider_radius))
        setattr(slider, 'mouseMoveEvent', self.mouseMoveEvent)
        setattr(slider, 'mousePressEvent', self.mousePressEvent)
        setattr(slider, 'mouseReleaseEvent', self.mouseReleaseEvent)

        return slider


    def _move(self, shift: int):
        shift = shift - self.slider_radius//2

        if shift <= self._get_slider_min_position():
            self.slider_position = self._get_slider_min_position()
        
        elif shift >= self._get_slider_max_position():
            self.slider_position = self._get_slider_max_position()

        else:
            self.slider_position = shift 
        
        self._slider.setGeometry(QtCore.QRect(self.slider_position, self._get_slider_y(), self.slider_radius, self.slider_radius))
        self._foreground_line.setGeometry(QtCore.QRect(self.x, self.y, self.slider_position-self.x, self.height))


    def mouseMoveEvent(self, event):
        if self.lmb_presed:
            self._move(event.globalX()-self._get_parent_window_x())
            
            # Проверка изменилось ли положение ползунка  
            if self.__dict__.get('last_position') != self._get_slider_position():
                self.changeEvent(event)

        super().mouseMoveEvent(event)


    def mousePressEvent(self, event):
        if(event.button() == QtCore.Qt.LeftButton):
            # Переменная start_position, нужна для проверки изменилась ли позиция слайдера после отжатия клавиши мышки
            self.__dict__.update({'lmb_presed': True, 'last_position': self._get_slider_position()})
        else:
            self.__dict__.update({'lmb_presed': False})

        self._slider.setCursor(QtCore.Qt.PointingHandCursor)
        super().mousePressEvent(event)


    def mouseReleaseEvent(self, event):
        self.__dict__.update({'lmb_presed': False})
        self._slider.setCursor(QtCore.Qt.ArrowCursor)
        
        super().mouseReleaseEvent(event)


    def changeEvent(self, event):
        self.valueChanged.emit(self.getValue())
        
        super().changeEvent(event)


    def setValue(self, position: int):
        if not isinstance(position, int):
            raise ValueError

        steps = self.max_value-self.min_value
        tick = steps/self._get_slider_width()

        self._move(self.x+int(position/tick))

        self.valueChanged.emit(self.getValue())


    def setMinimum(self, min_value: int):
        if not isinstance(min_value, int):
            raise ValueError

        self.min_value = min_value


    def setMaximum(self, max_value: int):
        if not isinstance(max_value, int):
            raise ValueError

        self.max_value = max_value


    def getValue(self):
        steps = self.max_value-self.min_value
        tick = steps/self._get_slider_width()

        return int(self.min_value+self._get_slider_position()*tick)


    def hide(self):
        self._background_line.hide()
        self._foreground_line.hide()
        self._slider.hide()


    def show(self):
        self._background_line.show()
        self._foreground_line.show()
        self._slider.show()


    def delete(self):
        self._background_line.deleteLater()
        self._foreground_line.deleteLater()
        self._slider.deleteLater()
        self.deleteLater()


class PlayButton(ClickedQLabel, BaseButtonEvents):
    """ Кнопка начала воспроизведения аудио """
    def __init__(self, *args, **kwargs):
        super(ClickedQLabel, self).__init__(*args, **kwargs)

        self.pixmap = QtGui.QPixmap(os.path.join('images', 'play.png'))
        self.pixmap_enter = self.pixmap.copy(14, 0, 28, 17)
        self.pixmap_leave = self.pixmap.copy(0, 0, 14, 17)
        self.setPixmap(self.pixmap_leave)


class PauseButton(ClickedQLabel, BaseButtonEvents):
    """ Кнопка остановки воспроизведения аудио """
    def __init__(self, *args, **kwargs):
        super(ClickedQLabel, self).__init__(*args, **kwargs)

        self.pixmap = QtGui.QPixmap(os.path.join('images', 'pause.png'))
        self.pixmap_enter = self.pixmap.copy(14, 0, 28, 17)
        self.pixmap_leave = self.pixmap.copy(0, 0, 14, 17)
        self.setPixmap(self.pixmap_leave)


class PlaylistButton(ClickedQLabel, BaseButtonEvents):
    """ Кнопка списка радиостанций """
    def __init__(self, *args, **kwargs):
        super(ClickedQLabel, self).__init__(*args, **kwargs)

        self.pixmap = QtGui.QPixmap(os.path.join('images', 'playlist.png'))
        self.pixmap_enter = self.pixmap.copy(23, 0, 46, 17)
        self.pixmap_leave = self.pixmap.copy(0, 0, 23, 17)
        self.setPixmap(self.pixmap_leave)


class PrevButton(ClickedQLabel, BaseButtonEvents):
    """ Кнопка включения предыдущей радиостанции """
    def __init__(self, *args, **kwargs):
        super(ClickedQLabel, self).__init__(*args, **kwargs)

        self.pixmap = QtGui.QPixmap(os.path.join('images', 'prev.png'))
        self.pixmap_enter = self.pixmap.copy(23, 0, 46, 17)
        self.pixmap_leave = self.pixmap.copy(0, 0, 23, 17)
        self.setPixmap(self.pixmap_leave)


class NextButton(ClickedQLabel, BaseButtonEvents):
    """ Кнопка включения следующей радиостанции """
    def __init__(self, *args, **kwargs):
        super(ClickedQLabel, self).__init__(*args, **kwargs)

        self.pixmap = QtGui.QPixmap(os.path.join('images', 'next.png'))
        self.pixmap_enter = self.pixmap.copy(23, 0, 46, 17)
        self.pixmap_leave = self.pixmap.copy(0, 0, 23, 17)
        self.setPixmap(self.pixmap_leave)


class MainForm(BaseForm):
    closeHandler = QtCore.pyqtSignal(dict)
    """ Главное окно радио """
    def __init__(self):
        super(BaseForm, self).__init__()
        self.form = QWidget()
        self.form.setFixedSize(336, 80)
        self.form.setObjectName('Form')

        self._customize_window()

        self.child_form = SelectRadioStationForm()

        self.font = QtGui.QFont()
        self.font.setFamily('Segoe UI Semibold')
        self.font.setPointSize(8)
        self.font.setWeight(75)
        self.font.setBold(True)

        self.playButton = self._make_play_button()
        self.pauseButton = self._make_pause_button()
        self.pauseButton.hide()
        self.prevButton = self._make_prev_button()
        self.nextButton = self._make_next_button()
        self.playlistButton = self._make_playlist_button()
        self.playlistButton.clicked.connect(self.select_station_form)
        self.volumeSlider = self._make_slider()

        self.form.show()
        QtCore.QMetaObject.connectSlotsByName(self.form)


    def _make_play_button(self):
        playButton = PlayButton(self.form)
        playButton.setGeometry(QtCore.QRect(46, 44, 14, 17))
        playButton.setObjectName('playButton')
        playButton.setToolTip('Играть')

        return playButton


    def _make_pause_button(self):
        pauseButton = PauseButton(self.form)
        pauseButton.setGeometry(QtCore.QRect(46, 44, 14, 17))
        pauseButton.setObjectName('pauseButton')
        pauseButton.setToolTip('Остановить')

        return pauseButton


    def _make_prev_button(self):
        prevButton = PrevButton(self.form)
        prevButton.setGeometry(QtCore.QRect(15, 44, 23, 17))
        prevButton.setObjectName('prevButton')
        prevButton.setToolTip('Предыдущая радиостанция')

        return prevButton


    def _make_next_button(self):
        nextButton = NextButton(self.form)
        nextButton.setGeometry(QtCore.QRect(70, 44, 23, 17))
        nextButton.setObjectName('nextButton')
        nextButton.setToolTip('Следующая радиостанция')

        return nextButton


    def _make_playlist_button(self):
        playlistButton = PlaylistButton(self.form)
        playlistButton.setFont(self.font)
        playlistButton.setGeometry(QtCore.QRect(110, 44, 23, 17))
        playlistButton.setObjectName('playlistButton')
        playlistButton.setToolTip('Список радиостанций')

        return playlistButton


    def _make_slider(self):
        slider = CustomSlider(self.form, 145, 50, 180)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(60)

        return slider


    def closeEvent(self):
        """ Переназначение базового метода closeEvent класcа BaseForm """
        try:
            config = {}
            config['last_volume'] = self.get_position_volume_slider()
            config['last_radio_station_name'] = self.get_title()
            
            self.closeHandler.emit(config)

        except (PermissionError, TypeError):
            show_error('Возникла критическая ошибка', 
                'Не удалось сохранить текущую конфигурацию плейера')
            
            if show_question('Возникла критическая ошибка', 'Выйти без сохранения текущей конфигурации?'):
                self.close()
        else:
            self.close()


    @property
    def child(self):
        return self.child_form


    def show_play_button(self):
        self.playButton.show()


    def hide_play_button(self):
        self.playButton.hide()


    def show_pause_button(self):
        self.pauseButton.show()

    
    def hide_pause_button(self):
        self.pauseButton.hide()

    
    def set_position_volume_slider(self, value):
        return self.volumeSlider.setValue(value)


    def get_position_volume_slider(self):
        return self.volumeSlider.getValue()


    def select_station_form(self):
        self.child_form.show()


    def selected_station(self):
        return self.child_form.get_selected_station()

 
class SelectRadioStationForm(BaseForm):
    callback = QtCore.pyqtSignal(str)
    """ Форма выбора радиостанции """
    def __init__(self):
        super().__init__()
        self.form = QWidget()
        self.form.setFixedSize(336, 125)
        self.form.setObjectName('Form')
        self.form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # Кастомизация базового окна
        self._customize_window()
        self.set_title('Выбор радиостанции')

        self.child_form = AppendStationForm()

        self.font = QtGui.QFont()
        self.font.setFamily('Segoe UI Semibold')
        self.font.setPointSize(8)
        self.font.setWeight(75)
        self.font.setBold(True)

        self.label = QLabel(self.form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QtCore.QRect(10, 35, 181, 16))
        self.label.setText('Все радиостанции')
        self.label.setStyleSheet('color: rgb(255, 255, 255);')

        self.comboBox_1 = QComboBox(self.form)
        self.comboBox_1.setObjectName(u"comboBox_1")
        self.comboBox_1.setGeometry(QtCore.QRect(10, 60, 316, 22))
        # Добавляет радиостанции в выпадающий список 
        self.update_combobox(utils.RADIO_STATIONS)

        self.appendStationButton = QPushButton(self.form)
        self.appendStationButton.setFont(self.font)
        self.appendStationButton.setGeometry(QtCore.QRect(10, 85, 142, 32))
        self.appendStationButton.setText('Добавить радиостанцию')
        self.appendStationButton.setStyleSheet('color: rgb(255, 255, 255);')
        self.appendStationButton.setFlat(True)
        self.appendStationButton.clicked.connect(self.append_station_window_show)

        self.deleteStationButton = QPushButton(self.form)
        self.deleteStationButton.setFont(self.font)
        self.deleteStationButton.setGeometry(QtCore.QRect(200, 85, 63, 32))
        self.deleteStationButton.setText('Удалить')
        self.deleteStationButton.setStyleSheet('color: rgb(255, 255, 255);')
        self.deleteStationButton.setFlat(True)
        self.deleteStationButton.clicked.connect(self.delete_station)

        self.listenStationButton = QPushButton(self.form)
        self.listenStationButton.setFont(self.font)
        self.listenStationButton.setGeometry(QtCore.QRect(265, 85, 63, 32))
        self.listenStationButton.setText('Слушать')
        self.listenStationButton.setStyleSheet('color: rgb(255, 255, 255);')
        self.listenStationButton.setFlat(True)
        self.listenStationButton.clicked.connect(self.listen_radiostation)

        QtCore.QMetaObject.connectSlotsByName(self.form)


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
                # Добавление имени и адреса радиостанции в глобальный словарь модуля utils
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
        self.child_form.callback.connect(self.append_station)
        self.child_form.show()


    def get_selected_station(self):
        """ Возвращает выбранную радиостанцию """
        return self.comboBox_1.currentText()


    def listen_radiostation(self):
        """ Передает выбранную радиостанцию в callback функцию """
        self.callback.emit(self.get_selected_station())


class AppendStationForm(BaseForm):
    callback = QtCore.pyqtSignal(str, str)
    """ Окно добавления новой радиостанции """
    def __init__(self):
        super().__init__()
        self.form = QWidget()
        self.form.setFixedSize(336, 155)
        self.form.setObjectName('Form')
        # Кастомизация базового окна
        self._customize_window()
        self.set_title('Добавление новой радиостанции')

        self.font = QtGui.QFont()
        self.font.setFamily('Segoe UI Semibold')
        self.font.setPointSize(8)
        self.font.setWeight(75)
        self.font.setBold(True)

        self.label = QLabel(self.form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QtCore.QRect(10, 35, 316, 16))
        self.label.setStyleSheet('color: rgb(255, 255, 255);')

        self.nameLineEdit = QLineEdit(self.form)
        self.nameLineEdit.setObjectName(u"nameLineEdit")
        self.nameLineEdit.setGeometry(QtCore.QRect(10, 95, 316, 21))
        self.nameLineEdit.setPlaceholderText('Имя радиостанции')

        self.urlLineEdit = QLineEdit(self.form)
        self.urlLineEdit.setObjectName(u"urlLineEdit")
        self.urlLineEdit.setGeometry(QtCore.QRect(10, 60, 316, 21))
        self.urlLineEdit.setPlaceholderText('URL адрес')

        self.closeButton = QPushButton(self.form)
        self.closeButton.setFont(self.font)
        self.closeButton.setGeometry(QtCore.QRect(200, 120, 63, 32))
        self.closeButton.setStyleSheet('color: rgb(255, 255, 255);')
        self.closeButton.setObjectName('pushButton_2')
        self.closeButton.setFlat(True)
        self.closeButton.clicked.connect(self.clearn_fields_and_hide)

        self.addButton = QPushButton(self.form)
        self.addButton.setFont(self.font)
        self.addButton.setGeometry(QtCore.QRect(265, 120, 63, 32))
        self.addButton.setStyleSheet('color: rgb(255, 255, 255);')
        self.addButton.setObjectName('addButton')
        self.addButton.setFlat(True)
        self.addButton.clicked.connect(self.append_station)

        self._retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.form)

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
            self.callback.emit(radio_station_name, radio_station_url)
            self._clearn_all_fields()
            self.hide()


    def clearn_fields_and_hide(self):
        """ Скрытие формы добавления радиостанции с очисткой полей """
        self._clearn_all_fields()
        self.hide()

