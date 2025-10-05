from classes import *


def main():
    win = Tk()
    
    nb = TimerWithSettings(win)
    nb.pack(fill=BOTH)

    win.mainloop()
        

if __name__ == '__main__':
    main()
