from tkinter import *

class AutoScrollbar(Scrollbar):
    # a scrollbar that hides itself if it's not needed.  only
    # works if you use the grid geometry manager.
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)
    # def pack(self, **kw):
    #     raise TclError, "cannot use pack with this widget"
    # def place(self, **kw):
    #     raise TclError, "cannot use place with this widget"

def make_canvas(root,row,column,root2):
    vscrollbar = AutoScrollbar(root)
    vscrollbar.grid(row=row, column=column+1, sticky=N+S)
    hscrollbar = AutoScrollbar(root, orient=HORIZONTAL)
    hscrollbar.grid(row=row+1, column=column, sticky=E+W)

    canvas = Canvas(root,xscrollcommand=hscrollbar.set,
                    yscrollcommand=vscrollbar.set)
    canvas.grid(row=row, column=column, sticky=N+S+E+W)

    vscrollbar.config(command=canvas.yview)
    hscrollbar.config(command=canvas.xview)

    # make the canvas expandable
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # create canvas contents

    frame = Frame(canvas)
    frame.rowconfigure(1, weight=1)
    frame.columnconfigure(1, weight=1)

    canvas.create_window(0, 0, anchor=NW, window=frame)

    frame.update_idletasks()

    canvas.config(scrollregion=(0,0,800,800))
    print(canvas.bbox(ALL))
    return frame