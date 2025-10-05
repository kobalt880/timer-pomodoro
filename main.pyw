from classes import *


def main():
    win = Tk()

    tf = TimeFrame(win)
    ts = TimeSettings(tf, win)
    
    tf.pack(side=LEFT)
    ts.pack(side=LEFT)
    
    win.mainloop()
        

if __name__ == '__main__':
    main()
