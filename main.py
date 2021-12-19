from tkinter import Tk, filedialog, W,E,N,S, StringVar, LEFT
from tkinter import ttk
from generate_plots import generate_plots

root = Tk()

class MainWindow:
    def __init__(self,root):
        root.title="Generate plots from .csv dataset"
        self.mainframe = ttk.Frame(root,padding=(12))
        self.mainframe.grid(column=0,row=0,sticky=(N, W))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        select_file_button = ttk.Button(
        self.mainframe,text="Select .csv file",
        command=self.select_csv
        )
        select_file_button.grid(column=0,row=0,sticky=E)

        self.selected_file_label = ttk.Label(self.mainframe,text="No file selected.")
        self.selected_file_label.grid(column=1,row=0,sticky=W)

        self.csv_file = None
        self.save_dir = None

        select_save_dir_button = ttk.Button(
        self.mainframe,text="Select plots destination folder",
        command=self.select_save_dir
        )
        select_save_dir_button.grid(column=0,row=1,sticky=E)

        self.selected_dir_label = ttk.Label(self.mainframe,text="Please, choose an empty folder.")
        self.selected_dir_label.grid(column=1,row=1,sticky=W)

        self.generate_button = ttk.Button(
            self.mainframe,
            text="Generate plots",
            command=self.generate_plots
        )

        self.generate_button.grid(row=2,column=0,columnspan=2,sticky=(E,W))

    def select_csv(self):
        file = filedialog.askopenfilename(
        filetypes=[("CSV dataset",".csv")]
        )
        self.csv_file = file
        self.selected_file_label['text'] = file.split('/')[-1]

    def select_save_dir(self):
        dir = filedialog.askdirectory()
        self.save_dir = dir
        self.selected_dir_label['text'] = dir

    def generate_plots(self):
        generate_plots(self.csv_file,self.save_dir)
MainWindow(root)
root.mainloop()
