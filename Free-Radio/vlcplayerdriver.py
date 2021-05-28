import vlc


class VlcPlayerDriver:
    """ Небольшая надстройка над библиотекой vlc """
    def __init__(self):
        self._source = None
        self._instance = vlc.Instance()
        self._mediaplayer = self._instance.media_player_new()


    def set_media(self, media):
        self._source = media


    def set_volume(self, value):
        if value in range(0, 101):
            self._mediaplayer.audio_set_volume(value)
        else:
            raise ValueError


    def play(self):
        self._media = self._instance.media_new(self._source)
        self._mediaplayer.set_media(self._media)
        self._mediaplayer.play()


    def pause(self):
        self._mediaplayer.pause()

