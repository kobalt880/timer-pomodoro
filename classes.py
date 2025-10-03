from tkinter import *
from threading import Thread
from time import sleep
from pygame import mixer
mixer.init()
sound = mixer.Sound('sound.wav')


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
        m = self._seconds // 60
        s = self._seconds - m * 60

        return (f'{"0" if m < 10 else ""}{m}:'
                f'{"0" if s < 10 else ""}{s}')


class PomodoroCycle:
    def __init__(self, work_tick_func, break_tick_func, work_end_func,
                 break_end_func, cycle_end_func, break_time: int = 300,
                 long_break_time: int = 1200, work_time: int = 1500,
                 iter_count: int = 4):
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
        

class TimeFrame(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columnconfigure([0, 1, 2], weight=1)
        self.rowconfigure([0, 1], weight=1)
        self._create_widgets()
        
        self._pc = None
        self._cycle_count = 0
        
        self._set_status('-')
        self._increase_cycle_count()

    def _create_widgets(self):
        self._status_label = Label(self)
        self._cycle_count_label = Label(self)
        self._time_label = Label(self, text='00:00', font=('arial', 30))
        launch_button = Button(self, text='Запустить', command=self.launch)
        reset_button = Button(self, text='Сбросить', command=self.reset)
        stop_button = Button(self, text='Остановить', command=self.stop)

        self._status_label.grid(column=0, row=0, sticky=W)
        self._cycle_count_label.grid(column=0, row=1, sticky=W)
        self._time_label.grid(column=0, row=2, padx=20, pady=20, columnspan=3)
        launch_button.grid(column=0, row=3, pady=10, padx=5)
        reset_button.grid(column=1, row=3, pady=10, padx=5)
        stop_button.grid(column=2, row=3, pady=10, padx=5)

    def launch(self):
        if self._pc is None:
            self._pc = PomodoroCycle(self._upd_time, self._upd_time,
            self._work_end, self._break_end, self.launch,
            30, 160, 60)
            self._pc.launch()
            self._set_status('Работа')
        else:
            self._pc.launch()

    def reset(self):
        self._pc.stop()
        self._pc = None
        self._set_time('00:00')
        self._set_status('-')
        self._cycle_count = 0
        self._increase_cycle_count()

    def stop(self):
        if self._pc is not None:
            self._pc.stop()

    def _work_end(self):
        sound.play()
        self._set_status('Перерыв')

    def _break_end(self):
        sound.play()
        self._increase_cycle_count()
        self._set_status('Работа')

    def _upd_time(self):
        text = str(self._pc.get_timer())
        self._set_time(text)

    def _set_time(self, time: str):
        self._time_label.configure(text=time)

    def _set_status(self, status: str):
        self._status_label.configure(text=f'Статус: {status}')

    def _increase_cycle_count(self):
        self._cycle_count += 1
        text = 'Помодоро № ' + str(self._cycle_count)
        self._cycle_count_label.configure(text=text)




    
