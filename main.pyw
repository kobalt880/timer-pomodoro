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
        print(pc)

    pc = PomodoroCycle(tick, tick, work_end, break_end, cycle_end, 15, 5, 20)
    pc.launch()
    
    while during:
        sleep(5)
        pc.launch()
        sleep(5)
        pc.stop()
        

if __name__ == '__main__':
    main()
