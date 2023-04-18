import tkinter as tk
from styles import Theme

class DataList:
    """ Simulates a datalist in HTML. Requires a Frame and some data in the type list. """


    def __init__(self, datalist_frame: tk.Frame, data: list, theme: Theme=Theme(), width=None, *args, **kwargs) -> None:
        self.__all_data = data
        self.__new_data = []

        self.__entry = tk.Entry(datalist_frame, relief="flat", background=theme.background, foreground=theme.foreground, highlightbackground=theme.border, highlightthickness=1, insertbackground=theme.foreground, width=width, font=("tkDefaultFont", 14))
        self.__entry.bind("<KeyRelease>", lambda event: self.show_new_data())
        self.__entry.pack(fill="x")

        self.__listbox = tk.Listbox(datalist_frame, relief="flat", background=theme.background, foreground=theme.foreground, highlightbackground=theme.border, highlightthickness=1, width=width, font=("tkDefaultFont", 14))
        self.__listbox.bind("<<ListboxSelect>>", lambda event: self.insert_selected_data())
        self.__listbox.pack(fill="x")

        self.show_new_data()


    def get_new_list(self) -> None:
        """ Once a character is entered, insert the new data into the listbox. """

        self.__new_data = []
        for data in self.__all_data:
            if self.__entry.get().lower() in str(data).lower():
                self.__new_data.append(data)
        return


    def get_selected(self) -> str:
        """ Return the chosen data outside the scope of the object. """

        return self.__entry.get()

    
    def insert_selected_data(self) -> None:
        """ Insert the selected data from the listbox into the entry. """

        if self.__listbox.curselection() == None:
            return

        self.__entry.delete("0", "end")
        self.__entry.insert("0", self.__listbox.get(self.__listbox.curselection()))
        self.__listbox.pack_forget()
        return

    
    def show_new_data(self) -> None:
        """ If there are any characters in the entry, display the listbox. If not, then hide the listbox. """

        if len(self.__entry.get()) != 0:
            self.get_new_list()
            self.__listbox.config(listvariable=tk.Variable(value=self.__new_data))
            self.__listbox.pack(fill="x")
        else:
            self.__listbox.pack_forget()
        return