import json
from tkinter import *
from urllib.request import urlopen

sel = list()


# First create application class
class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.pack()
        self.create_widgets()

    def CurSelet(self, evt):
        global sel
        temp = list()
        for i in self.lbox.curselection():
            temp.append(self.lbox.get(i))

        allitems = list()
        for i in range(self.lbox.size()):
            allitems.append(self.lbox.get(i))

        for i in sel:
            if i in allitems:
                if i not in temp:
                    sel.remove(i)

        for x in self.lbox.curselection():
            if self.lbox.get(x) not in sel:
                sel.append(self.lbox.get(x))

    def select(self):
        exit(0)

    # Create main GUI window
    def create_widgets(self):
        self.search_var = StringVar()
        self.search_var.trace("w", lambda name, index, mode: self.update_list())
        self.entry = Entry(self, textvariable=self.search_var, width=50)
        self.lbox = Listbox(self, selectmode=SINGLE, width=50, height=15)
        self.lbox.bind('<<ListboxSelect>>', self.CurSelet)

        self.entry.grid(row=0, column=0, padx=14, pady=3)
        self.lbox.grid(row=1, column=0, padx=14, pady=3)

        self.btn = Button(self, text='Излезни', command=self.select, width=20)
        self.btn.grid(row=2, column=0, padx=14, pady=3)

        # Function for updating the list/doing the search.
        # It needs to be called here to populate the listbox.
        self.update_list()

    def get_articles_list(self):
        url = 'http://94.156.140.187/bm_codes.json'
        json_url = urlopen(url)
        data = json.loads(json_url.read())
        return dict(data) if len(data) else False

    def update_list(self):
        global sel
        global l
        search_term = self.search_var.get()

        # Just a generic list to populate the listbox
        lbox_list = [f'[ {int(code):04d} ]   {name}' for name, code in self.get_articles_list().items()]

        self.lbox.delete(0, END)

        for item in lbox_list:
            if search_term.lower() in item.lower():
                self.lbox.insert(END, item)

        allitems = list()
        for i in range(self.lbox.size()):
            allitems.append(self.lbox.get(i))

        for i in sel:
            if i in allitems:
                self.lbox.select_set(self.lbox.get(0, "end").index(i))


root = Tk()
root.title('БМ Маркет (Раковска) - търсачка за номера на артикули')
Label(root, text='Търсене на код по име на артикул:').pack()
app = Application(master=root)
print('Starting mainloop()')
app.mainloop()
