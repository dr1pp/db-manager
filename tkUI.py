from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from tkinter import ttk


def initUI(startPage):
    root = Root()
    root.page = startPage(root)
    root.page.frame.pack()
    root.page.display()
    root.mainloop()
    root.destroy()


class UI:
    def __init__(self, startPage):
        self.root = Root()
        self.root.page = startPage(self.root)
        self.root.page.frame.pack()
        self.root.page.display()
        self.root.mainloop()
        self.root.destroy()

class Root(Tk):
    def __init__(self):
        super().__init__()
        self.page = None
        self.menuBar = MenuBar(self)
        self.menuBar.pack()

class WindowRoot(Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.page = None
        self.menuBar = MenuBar(self)
        self.menuBar.pack()

    def refreshParent(self):
        try:
            self.parent.refresh()
        except:
            pass


class MenuBar(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.master = parent
        self.menuBar = Menu(self.master)

class Container():
    def __init__(self, master, parent):
        self.master = master
        self.parent = parent

class FrameStruct():
    def __init__(self, master, parent, *args, **kwargs):
        self.frame = Frame(parent.frame, *args, **kwargs)
        self.master = master
        self.parent = parent
        self.args = args
        self.kwargs = kwargs

    def refresh(self):
        self.frame.destroy()
        self.frame = Frame(self.parent.frame, *self.args, **self.kwargs)
        self.display()

    def refreshParent(self):
        self.parent.refresh()
        self.frame = Frame(self.parent.frame, *self.args, **self.kwargs)
        self.display()

class TtkFrameStruct:
    def __init__(self, master, parent, *args, **kwargs):
        self.frame = ttk.Frame(parent.frame)
        self.master = master
        self.parent = parent
        self.args = args
        self.kwargs = kwargs

class Page:
    def __init__(self, master, parent=None):
        self.master = master
        self.parent = parent
        self.frame = self.getFrame(self.master)

    def goTo(self, page, *args, **kwargs):
        if not isinstance(page(self.master, *args, **kwargs), Page):
            raise TypeError("'newPage' must be subclass of 'Page'")
        self.master.page = page(self.master, *args, **kwargs)
        self.master.page.frame.pack()
        self.destroy()
        self.master.page.display()

    def open(self, page, *args, **kwargs):
        parent = self.master.page
        if not isinstance(page(self.master, *args, **kwargs), Page):
            raise TypeError("'window' must be subclass of 'Page'")
        newWindow = WindowRoot(parent)
        newWindow.page = page(newWindow, *args, **kwargs)
        newWindow.page.frame.pack()
        newWindow.page.display()

    def embed(self, page, *args, **kwargs):
        newPage = page(self.frame, *args, **kwargs)
        newPage.display()
        return newPage.frame

    def refresh(self):
        self.frame.destroy()
        self.frame = self.getFrame(self.master)
        self.frame.pack()
        self.master.page.display()

    def destroy(self):
        self.frame.destroy()

    def getFrame(self, master):
        if not isinstance(master, Root) and not isinstance(master, Toplevel) and not isinstance(master,
                                                                                                Frame) and not isinstance(
                master, FrameStruct):
            raise TypeError("'master' must be instance of 'Root' or 'Window'")
        frame = Frame(master)
        return frame