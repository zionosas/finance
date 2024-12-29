from tkinter import Tk

from user import users


class main:
    def __init__(self):
        root = Tk()
        self.root.iconbitmap('RCCGpx.ico')
        self.app = users(root)
        root.mainloop()


if __name__ == "__main__":
    main()


