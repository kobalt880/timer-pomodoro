from classes import *


def main():
    win = Tk()
    
    pt = PolyTimer(win)
    pt.pack(fill=BOTH)

    win.mainloop()
        

if __name__ == '__main__':
    main()
