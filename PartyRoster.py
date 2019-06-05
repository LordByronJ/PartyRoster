from tkinter import *
from tkinter import messagebox
from functools import partial

import sqlite3


class DB():
    def __init__(self):
        pass

    def create(self):
        conn = sqlite3.connect('db.db')
        cur = conn.cursor()
        cur.execute("""CREATE TABLE def
        (
            cat text,
            name text
        )""")
        conn.commit()
        conn.close()

    def add(self, cat, name):
        conn = sqlite3.connect('db.db')
        cur = conn.cursor()
        with conn:
            cur.execute("INSERT INTO def VALUES (?, ?)", (cat, name))
        print("adding")
        conn.close()

    def remove(self, cat, name):
        conn = sqlite3.connect('db.db')
        cur = conn.cursor()
        with conn:
            cur.execute("DELETE FROM def WHERE cat LIKE ? AND name LIKE ?", (cat, name))
        print("removing")
        conn.close()

    def findPerson(self, type_, info):
        conn = sqlite3.connect('db.db')
        cur = conn.cursor()
        with conn:
            cur.execute("SELECT * FROM def WHERE ? LIKE ? ", (type_, info))
            s = cur.fetchall()
        conn.close()
        return s


class ScrollFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent)  # create a frame (self)

        self.canvas = Canvas(self, borderwidth=0, background="#ffffff")  # place canvas on self
        self.viewPort = Frame(self.canvas,
                              background="#ffffff")  # place a frame on the canvas, this frame will hold the child widgets
        self.vsb = Scrollbar(self, orient="vertical",
                             command=self.canvas.yview)  # place a scrollbar on self
        self.canvas.configure(yscrollcommand=self.vsb.set)  # attach scrollbar action to scroll of canvas

        self.vsb.pack(side="right", fill="y")  # pack scrollbar to right of self
        self.canvas.pack(side="left", fill="both", expand=True)  # pack canvas to left of self and expand to fil
        self.canvas.create_window((4, 4), window=self.viewPort, anchor="nw",  # add view port frame to canvas
                                  tags="self.viewPort")

        self.viewPort.bind("<Configure>",
                           self.onFrameConfigure)  # bind an event whenever the size of the viewPort frame changes.

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox(
            "all"))  # whenever the size of the frame changes, alter the scroll region respectively.


class Rosters(Frame):

    def __init__(self, root, db):
        Frame.__init__(self, root)
        self.tk = root
        self.db = db
        self.defList = list()
        self.mayList = list()
        self.labels = list()
        self.rows = list()
        self.scrollFrame = ScrollFrame(root)

        self.listFrame = Frame(self.scrollFrame.viewPort, borderwidth=1, relief='solid')
        self.listFrame.pack(side=LEFT, fill=Y)
        self.buttonsFrame = Frame(self.scrollFrame.viewPort)
        self.buttonsFrame.pack(side=RIGHT, fill=Y)

        self.addUI(self.buttonsFrame)
        for s in self.db.findPerson("%", "%"):
            if s[0] == "def":
                self.defList.append(s[1])
            elif s[0] == "may":
                self.mayList.append(s[1])
        self.update()

    def remove_maybe(self):
        s = self.enD.get().upper()
        s = s.strip()
        if len(s) == 0:
            pass
        elif not self.mayList.__contains__(s.upper()):
            messagebox.showinfo("Not Contained", s)
        else:
            self.enD.delete(0, "end")
            self.enD.insert(0, "")
            self.mayList.remove(s.upper())
            self.db.remove("may", s)
            self.update()
        return s

    def remove_definitely(self):
        s = self.enD.get().upper()
        s = s.strip()
        if len(s) == 0:
            pass
        elif not self.defList.__contains__(s.upper()):
            messagebox.showinfo("Not Contained", s)
        else:
            self.enD.delete(0, "end")
            self.enD.insert(0, "")
            self.defList.remove(s.upper())
            self.db.remove("def", s)
            self.update()
        return s

    def add_maybe(self):
        s = self.enD.get().upper()
        s = s.strip()
        if len(s) == 0:
            pass
        elif self.mayList.__contains__(s.upper()):
            messagebox.showinfo("Alredy Contained", s)
        else:
            self.enD.delete(0, "end")
            self.enD.insert(0, "")
            self.mayList.append(s.upper())
            self.db.add("may", s)
            self.update()
        return s

    def add_definitely(self):
        s = self.enD.get().upper()
        s = s.strip()
        if len(s) == 0:
            pass
        elif self.defList.__contains__(s.upper()):
            messagebox.showinfo("Alredy Contained", s)
        else:
            self.enD.delete(0, "end")
            self.enD.insert(0, "")
            self.defList.append(s.upper())
            self.db.add("def", s)
            self.update()
        return s

    def transfer_from_maybe(self):
        s = self.remove_maybe()
        definitely_string = self.enD.get().strip()
        self.enD.delete(0, "end")
        self.enD.insert(0, s)
        self.add_definitely()
        self.enD.delete(0, "end")
        self.enD.insert(0, definitely_string)

    def transfer_from_definitely(self):
        s = self.remove_definitely()
        maybe_string = self.enD.get().strip()
        self.enD.delete(0, "end")
        self.enD.insert(0, s)
        self.add_maybe()
        self.enD.delete(0, "end")
        self.enD.insert(0, maybe_string)

    def update(self):
        root = self.listFrame
        self.defList.sort()
        self.mayList.sort()
        for l in self.labels:
            l.destroy()
        for row in self.rows:
            row.destroy()
        self.rows = list()
        for i in range(max(len(self.defList), len(self.mayList))):
            row = Frame(root, height=2)
            row.pack(fill=X, padx=5, pady=5)
            self.rows.append(row)
        h = 0
        for s in self.defList:
            guest_name = Label(self.rows[h], text=(s), width=15, anchor='w')
            guest_name.pack(side=LEFT, anchor="w")
            self.labels.append(guest_name)
            h = h + 1
        h = 0
        for s in self.mayList:
            guest_name = Label(self.rows[h], text=(s), width=15, anchor='e')
            guest_name.pack(side=RIGHT, anchor="e")
            self.labels.append(guest_name)
            h = h + 1
        self.defCount['text'] = str(len(self.defList))
        self.mayCount['text'] = str(len(self.mayList))

        self.scrollFrame.pack(side='top', fill='both', expand=True)

    def addUI(self, root):
        """
            Creates UI elements, like imput and buttons
            Parameters:
                The tk object
        """

        self.enD = Entry(root)
        self.enD.pack(anchor="e", padx=20, pady=10)

        button = Button(root, text="Submit to Definitely Invite List",
                        command=partial(self.add_definitely, ))
        button.pack(anchor="e", padx=20, pady=10)

        button = Button(root, text="Remove from Definitely Invite List",
                        command=partial(self.remove_definitely, ))
        button.pack(anchor="e", padx=20, pady=10)

        button = Button(root, text="Submit to Maybe Invite List", command=partial(self.add_maybe, ))
        button.pack(anchor="e", padx=20, pady=10)
        button = Button(root, text="Transfer to Maybe Invite List", command=partial(self.transfer_from_definitely, ))
        button.pack(anchor="e", padx=20, pady=10)

        button = Button(root, text="Submit to Maybe Invite List", command=partial(self.add_maybe, ))
        button.pack(anchor="e", padx=20, pady=10)

        button = Button(root, text="Remove from Maybe Invite List",
                        command=partial(self.remove_maybe, ))
        button.pack(anchor="e", padx=20, pady=10)

        button = Button(root, text="Transfer to Definitely list", command=partial(self.transfer_from_maybe, ))
        button.pack(anchor="e", padx=20, pady=10)

        th = Button(root, text="quit", command=self.quit_app)
        th.pack(anchor="e", padx=20, pady=10)

        self.defCount = Label(root, text=str(len(self.defList)))
        self.defCount.pack(anchor="e", padx=20, pady=10)

        self.mayCount = Label(root, text=str(len(self.mayList)))
        self.mayCount.pack(anchor="e", padx=20, pady=10)

    @staticmethod
    def quit_app():
        """
            Stops the application
        """
        exit()


def main():
    """
        Main Method
    """
    db = DB()
    root = Tk()
    size = "500x500"
    root.geometry(size)
    win = Rosters(root, db)
    root.mainloop()


def remove_all():
    db = DB()
    db.remove("%", "%")


if __name__ == '__main__':
    main()
