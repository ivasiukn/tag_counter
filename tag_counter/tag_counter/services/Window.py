import tkinter


class Window:
    top = None

    def __init__(self):
        self.top = tkinter.Tk()

    def open(self):
        self.top.mainloop()
