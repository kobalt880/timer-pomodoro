from tkinter import *
from threading import Thread
from time import sleep


class Timer:
    def __init__(self, seconds: int, tick_function, end_function):
        self._seconds = seconds
        self._end_function = end_function
        self._tick_function = tick_function
        self._pause = True
        self._during = False

    def _check_expired(self) -> bool:
        expired = self._seconds <= 0
        
        if expired:
            self._end_function()
            
        return expired

    def _time_cycle(self):
        self._during = True
        
        while not self._check_expired() and not self._pause:
            self._seconds -= 1
            self._tick_function()
            sleep(1)

        self._during = False
    
    def launch(self):
        self._pause = False
        if not self._during:
            Thread(target=self._time_cycle).start()

    def stop(self):
        self._pause = True

    def get_seconds(self) -> int:
        return self._seconds

    def __str__(self):
        h = self._seconds // 60 // 60
        m = self._seconds // 60 - h * 60
        s = self._seconds - m * 60 - h * 3600

        return (f'{"0" if h < 10 else ""}{h}:'
                f'{"0" if m < 10 else ""}{m}:'
                f'{"0" if s < 10 else ""}{s}')


class PomodoroCycle:
    def __init__(self, work_tick_func, break_tick_func, work_end_func,
                 break_end_func, cycle_end_func, break_time: int = 300,
                 long_break_time: int = 1200, work_time: int = 1500, iter_count: int = 4):
        self._break_time = break_time
        self._long_break_time = long_break_time
        self._work_time = work_time
        self._iter_count = iter_count
        self._ic_reserv = iter_count
        self._work_tick_func = work_tick_func
        self._break_tick_func = break_tick_func
        self._work_end_func = work_end_func
        self._break_end_func = break_end_func
        self._cycle_end_func = cycle_end_func
        self._timer = None

    def launch(self):
        if self._timer is None:
            self._start_time_cycle()
        else:
            self._timer.launch()

    def _start_time_cycle(self):
        self._start_work_cycle()

    def _start_break_cycle(self, long: bool):
        def break_func():
            self._break_end_func()
            
            if not long:
                self._iter_count -= 1
                self._start_work_cycle()
            else:
                self._timer = None
                self._iter_count = self._ic_reserv
                self._cycle_end_func()

        time = self._break_time if not long else self._long_break_time
        self._timer = Timer(time, self._break_tick_func, break_func)
        self._timer.launch()

    def _start_work_cycle(self):
        def work_func():
            self._work_end_func()
            self._start_break_cycle(self._iter_count == 1)
        
        self._timer = Timer(self._work_time, self._work_tick_func, work_func)
        self._timer.launch()

    def get_timer(self) -> Timer | None:
        return self._timer

    def stop(self):
        if self._timer is not None:
            self._timer.stop()

    def set_work_time(self, new_time: int):
        self._work_time = new_time

    def set_break_time(self, new_time: int):
        self._break_time = new_time

    def set_long_break_time(self, new_time: int):
        self._long_break_time = new_time

    def __str__(self):
        return str(self._timer)
        


