from classes import *


def main():
    def printer():
        print(t)

    def end():
        print('end')
    
    t = Timer(120, end, printer)
    t.launch()

    while t.get_seconds() != 0:
        sleep(5)
    

if __name__ == '__main__':
    main()
