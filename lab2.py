# Project Name: Lab 2:  Data Analysis/Visualization and GUI, using numpy, matplotlib, tkinter
# Name :        Yin Chang
# Discription:  Write a GUI application that lets the user look up the transfer rate of CA community colleges to the CSUs.
# Module:       lab2.py
# Discription:  provides the GUI to interact with the user by providing 3 windows

import tkinter.messagebox as tkmb
# normal import of pyplot to plot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Canvas widget
# normal import of tkinter for GUI
import tkinter as tk
from transfer import Transfer
import matplotlib
# tell matplotlib to work with Tkinter
matplotlib.use('TkAgg')


'''-------------------Defining dialogWin class--------------------'''


class dialogWin(tk.Toplevel):  # inherit from tkinter Tk class
    """ The Main Window, one title, explaination and 3 buttons"""

    def __init__(self, master):
        """ The constructor, set up the dialog window"""
        super().__init__(master)
        self.focus_set()       # It should have the focus.
        self.grab_set()        # The user should not be able to click on any plot window
        # or on the main window to start another event until the dialog window closes.
        self.transient(master)
        self.title("Choose Colleges")
        scrollb = tk.Scrollbar(self)
        self._listB = tk.Listbox(
            self, height=10, width=40, selectmode="multiple", yscrollcommand=scrollb.set)
        ccList = master._transferObj.getCC()
        self._listB.insert(tk.END, *ccList)
        scrollb.config(command=self._listB.yview)
        self._listB.grid(row=0, column=0)
        scrollb.grid(row=0, column=1, sticky='ns')

        L = self._listB.curselection()
        tk.Button(self, text="OK", command=lambda: self._plotET(master)).grid()

    def _plotET(self, master):
        L = self._listB.curselection()
        pltWin = plotWin(master, self, 3, L)
        self.destroy()  # If the user clicks OK to lock in the choice, then the dialog window closes


'''-------------------Defining plotWin class--------------------'''


class plotWin(tk.Toplevel):	         # inherit from tkinter Tk class
    """ The Main Window, one title, explaination and 3 buttons"""

    def __init__(self, master, decision, *arg):
        """ The constructor, set up the plot window"""
        super().__init__(master)
        self.transient(master)
        if decision == 1:
            self.title("Total Transfer Trend")
            fig = plt.figure(figsize=(5, 5))
            master._transferObj.plotTransferTrend()
            canvas = FigureCanvasTkAgg(fig, master=self)
            canvas.get_tk_widget().grid()
            canvas.draw()
        elif decision == 2:
            self.title("Top Transfer trend")
            fig = plt.figure(figsize=(8, 4))
            master._transferObj.plotTopTenTransfer()
            canvas = FigureCanvasTkAgg(fig, master=self)
            canvas.get_tk_widget().grid()
            canvas.draw()
        else:
            self.title("Enrollment Trend")
            fig = plt.figure(figsize=(8, 5))
            master._transferObj.plotEnrollmentTrend(*(arg[1]))
            canvas = FigureCanvasTkAgg(fig, master=self)
            canvas.get_tk_widget().grid()
            canvas.draw()


'''-------------------Defining mainWin class--------------------'''


class mainWin(tk.Tk):  # inherit from tkinter Tk class
    """ The Main Window, one title, explaination and 3 buttons"""

    def __init__(self):
        """ The constructor, set up the main window"""
        super().__init__()
        try:
            self._transferObj = Transfer()
            self.title("Transfer Rates")  # Set the Title
            # A line of text to explain what the application is
            tk.Label(self, text="Community College Transfer Rate to CSU",
                     fg="blue").grid(row=0, column=0, columnspan=3)
            tk.Button(self, text="Total Transfers", command=self._plotTotalTransfers).grid(
                column=0, columnspan=1)
            tk.Button(self, text="Top Ten", command=self._plotTopTen).grid(
                row=1, column=1, columnspan=1)
            tk.Button(self, text="Colleges", command=self._collegeList).grid(
                row=1, column=2, columnspan=1)
            self.protocol("WM_DELETE_WINDOW", self._endfct)
        except Exception as exceptObj:  # If any of the file open is not successful, a messagebox window will show up
            tkmb.showerror("Error", str(exceptObj), parent=self)
            self.destroy()  # Click X or OK to close the error window and the main window

    def _plotTotalTransfers(self):
        """ Create a plot window appears with the total transfer plot"""
        pltWin = plotWin(self, 1)  # 1 means user click the first button

    def _plotTopTen(self):
        """ Create a plot window appears with the top ten plot"""
        pltWin = plotWin(self, 2)  # 2 means user click the second button

    def _collegeList(self):
        """ Create a dialog window appears with the listbox. """
        colList = dialogWin(self)
        self.wait_window(colList)

    def _endfct(self):
        """ A function to confirm if user really want to quit"""
        askUser = tkmb.askokcancel(
            "Confirm", "Are you sure you want to quit?", parent=self)
        if askUser == True:
            self.destroy()
            print("GUI done")
            self.quit()


def main():
    """ A main function to create a main wondow object and run it"""
    a = mainWin()
    a.mainloop()


main()
