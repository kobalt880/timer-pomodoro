from classes import *


def main():
    during = True

    def cycle_end():
        nonlocal during
        during = False
        print('END')

    def work_end():
        print('work end')

    def break_end():
        print('break end')

    def tick():
        print(pc.get_timer())
    
    pc = PomodoroCycle(tick, tick, work_end, break_end, cycle_end, 1, 10, 2)
    pc.launch()

    while during:
        sleep(5)
    

if __name__ == '__main__':
    main()
