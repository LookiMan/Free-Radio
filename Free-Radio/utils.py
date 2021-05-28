import json
import shutil
import platform
import ctypes
from pathlib import Path



DEFAULT_RADIOS_JSON = Path(__file__).parent / "data" / "radios.json"


def get_screen_width():
    """ Получение ширины экрана """
    return ctypes.windll.user32.GetSystemMetrics(0)


def get_screen_height():
    """ Получение высоты экрана """
    return ctypes.windll.user32.GetSystemMetrics(1)


def get_config_directory():
    """ Получение пути к директории с конфигурацией """
    if platform.system() == 'Linux':
        config_dir = Path.home() / ".config" / "radio"

    elif platform.system() == 'Windows':
        config_dir = Path.home() / "radio"

    return config_dir


def load_config():
    """ Загрузка конфигурации радио """
    config_dir = get_config_directory()
    config_json = config_dir / "config.json"

    if config_json.exists():
        with config_json.open() as file:
            return json.load(file)
    else:
        return {}


def save_config(config: dict):
    """ Сохранение конфигурации радио """
    config_dir = get_config_directory()
    config_json = config_dir / "config.json"

    with config_json.open(mode='w') as file:
        json.dump(config, file, indent=4)


def load_radios():
    """ Загрузка радиостанций """
    config_dir = get_config_directory()
    radios_json = config_dir / "radios.json"
    
    if not radios_json.exists():
        
        if not config_dir.exists():
            config_dir.mkdir()
        
        with DEFAULT_RADIOS_JSON.open() as file:
            save_radios(json.load(file))
    
    with radios_json.open() as file:
        radios = json.load(file)
    
    return radios


def save_radios(radios: dict):
    """ Сохранение радиостанций """
    config_dir = get_config_directory()
    radios_json = config_dir / "radios.json"

    """ Сохранение радиостанций """
    with radios_json.open('w') as file:
        json.dump(radios, file, indent=4)


def append_new_radio_station(radio_station_name: str, radio_station_url: str):
    """ Добавление новой радиостанции """
    RADIO_STATIONS[radio_station_name] = radio_station_url

    save_radios(RADIO_STATIONS)


def delete_radio_station(radio_station_name: str):
    """ Удаление радиостанции """
    del RADIO_STATIONS[radio_station_name]

    save_radios(RADIO_STATIONS)


RADIO_STATIONS = load_radios()
