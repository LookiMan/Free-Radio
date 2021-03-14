import vlc


class VlcPlayerDriver:
    """ """
    def __init__(self):
        self._is_mute = False
        self._source = None
        self._instance = vlc.Instance()
        self._mediaplayer = self._instance.media_player_new()


    def is_mute(self):
        return self._is_mute


    def set_media(self, media):
        self._source = media


    def set_volume(self, value):
        if value in range(0, 101):
            self._mediaplayer.audio_set_volume(value)
        else:
            raise ValueError


    def set_mute_state(self, state: bool):
        if isinstance(state, bool):
            self._is_mute = state
            self._mediaplayer.audio_set_mute(self._is_mute)
        else:
            raise ValueError


    def play(self):
        self._media = self._instance.media_new(self._source)
        self._mediaplayer.set_media(self._media)
        self._mediaplayer.play()


    def pause(self):
        self._mediaplayer.pause()


    def stop(self):
        self._mediaplayer.stop()

