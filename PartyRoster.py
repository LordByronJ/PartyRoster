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
        )""" )
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

class Rosters(Frame):

    def __init__(self, root, db):
        Frame.__init__(self, root) 
        self.tk = root
        self.db = db
        self.defList = list()
        self.mayList = list()
        self.lables = list()
        self.addUI(root)
        for s in self.db.findPerson("%", "%"):
            if s[0] == "def":
                self.defList.append(s[1])
            elif s[0] == "may":
                self.mayList.append(s[1])
        self.update()
    
    def removeMay(self):
        s = self.enM.get().upper()
        s = s.strip()
        if len(s) == 0:
            pass
        elif  not self.mayList.__contains__(s.upper()):
            messagebox.showinfo("Not Contained", s)
        else:
            self.enM.delete(0, "end")
            self.enM.insert(0, "")
            self.mayList.remove(s.upper())
            self.db.remove("may", s)
            self.update()
        return s
    
    def removeDef(self):
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
    
    def addMay(self):
        s = self.enM.get().upper()
        s = s.strip()
        if len(s) == 0:
            pass
        elif self.mayList.__contains__(s.upper()):
            messagebox.showinfo("Alredy Contained", s)
        else: 
            self.enM.delete(0, "end")
            self.enM.insert(0, "")
            self.mayList.append(s.upper())
            self.db.add("may", s)
            self.update()
        return s
    
    def addDef(self):
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

    def transferfromMay(self):
        s = self.removeMay()
        defStringTemp = self.enD.get().strip()
        self.enD.delete(0, "end")
        self.enD.insert(0, s)
        self.addDef()
        self.enD.delete(0, "end")
        self.enD.insert(0, defStringTemp)

    def transferFromDef(self):
        s = self.removeDef()
        mayStringTemp = self.enM.get().strip()
        self.enM.delete(0, "end")
        self.enM.insert(0, s)
        self.addMay()
        self.enM.delete(0, "end")
        self.enM.insert(0, mayStringTemp)

    def update(self):
        self.defList.sort()
        self.mayList.sort()
        for l in self.lables:
            l.destroy()
        h = 1
        for s in self.defList:
            eleNum = Label(self.tk, text=(s))
            eleNum.place(x=10, y=20 * h, anchor = "w")
            self.lables.append(eleNum)
            h = h + 1
        h = 1
        for s in self.mayList:
            eleNum = Label(self.tk, text = (s))
            eleNum.place(x=250, y=20 * h, anchor = "center")
            self.lables.append(eleNum)
            h = h + 1
        self.defCount['text'] = str(len(self.defList))
        self.mayCount['text'] = str(len(self.mayList))
        
    def addUI(self, root):
        """
            Creates UI elements, like imput and buttons
            Parameters:
                The tk object
        """
        scrollbar = Scrollbar(root)
        scrollbar.pack(side="right", fill="y")

        self.enD = Entry(self.tk)
        self.enD.pack(anchor = "e", padx = 20, pady = 10)
        
        button = Button(self.tk, text="Submit to Definetly Invite List", command=partial(self.addDef,))
        button.pack(anchor = "e", padx = 20, pady = 10)
        
        button = Button(self.tk, text="Remove from Definetly Invite List", command = partial(self.removeDef, ))
        button.pack(anchor = "e", padx = 20, pady = 10)

        button = Button(self.tk, text="Transfer to Maybe Invite list", command = partial(self.transferFromDef, ))
        button.pack(anchor = "e", padx = 20, pady = 10)

        self.enM = Entry(self.tk)
        self.enM.pack(anchor = "e", padx = 20, pady = 10)
        
        button = Button(self.tk, text="Submit to Maybe Invite List", command = partial(self.addMay, ))
        button.pack(anchor = "e", padx = 20, pady = 10)
        
        button = Button(self.tk, text="Remove from Maybe Invite List", command = partial(self.removeMay, ))
        button.pack(anchor = "e", padx = 20, pady = 10)

        button = Button(self.tk, text="Transfer to Definetly list", command = partial(self.transferfromMay, ))
        button.pack(anchor = "e", padx = 20, pady = 10)

        th = Button(self.tk, text="quit", command = self.quitComm)
        th.pack(anchor = "e", padx = 20, pady = 10)

        self.defCount = Label(self.tk, text=str(len(self.defList)))
        self.defCount.pack(anchor = "e", padx = 20, pady = 10)

        self.mayCount = Label(self.tk, text=str(len(self.mayList)))
        self.mayCount.pack(anchor = "e", padx = 20, pady = 10)

    def quitComm(self):
        """
            Stops the application
        """
        exit()

def main():
    db = DB()
    root = Tk()
    size = "500x500"
    root.geometry(size)
    win = Rosters(root, db)
    root.mainloop()

def removeAll():
    db = DB()
    db.remove("%","%")

main()