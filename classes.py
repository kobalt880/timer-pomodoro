from tkinter import *
from threading import Thread
from time import sleep


class Timer:
    def __init__(self, seconds: int, end_function, tick_function):
        self._seconds = seconds
        self._end_function = end_function
        self._tick_function = tick_function

    def _check_expired(self) -> bool:
        expired = self._seconds <= 0
        
        if expired:
            self._end_function()
            
        return expired

    def _time_cycle(self):
        while not self._check_expired():
            self._seconds -= 1
            self._tick_function()
            sleep(1)
    
    def launch(self):
        Thread(target=self._time_cycle).start()

    def get_seconds(self) -> int:
        return self._seconds

    def __str__(self):
        h = self._seconds // 60 // 60
        m = self._seconds // 60 - h * 60
        s = self._seconds - m * 60 - h * 3600

        return (f'{"0" if h < 10 else ""}{h}:'
                f'{"0" if m < 10 else ""}{m}:'
                f'{"0" if s < 10 else ""}{s}')
