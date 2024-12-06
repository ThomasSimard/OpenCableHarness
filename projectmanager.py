"""Project manager window"""

from tkinter import ttk
from tkinter import filedialog
import tkinter as tk

import json
from json.decoder import JSONDecodeError

class ProjectWindow:
    """Let the user create and open projects"""

    def __init__(self, root):
        self.recent_project_label = tk.Label(root, text="Recent project:")
        self.recent_project_label.grid(row=0, column=0)

        self.recent_project_listbox = tk.Listbox(root, width=40)
        self.recent_project_listbox.grid(row=1, column=0, columnspan=2)

        self.recent_project_list = []
        self.load_recent_project()

        self.open_recent_project_button = tk.Button(root, text="Open recent project",
            command=self.open_recent_project)

        self.open_recent_project_button.grid(row=2, column=0, columnspan=2)

        self.search_project_button = tk.Button(root, text="Search project file",
            command=self.search_project)

        self.search_project_button.grid(row=3, column=0, columnspan=2)

        self.separator = ttk.Separator(root, orient='horizontal')
        self.separator.grid(row=4, column=0, columnspan=2, sticky="ew")

        self.create_project_label = tk.Label(root, text="Create project")
        self.create_project_label.grid(row=5, column=0, columnspan=2)

        self.project_name_label = tk.Label(root, text="Project name:")
        self.project_name_label.grid(row=6, column=0)

        self.project_name_entry = tk.Entry(root)
        self.project_name_entry.grid(row=7, column=1)

        self.new_project_button = tk.Button(root, text="Create new project",
            command=self.create_project)

        self.new_project_button.grid(row=8, column=0, columnspan=2)

    def load_recent_project(self):
        """Load recent projects"""

        with open("recent_project.txt", 'r', encoding='utf-8') as save_file:
            try:
                self.recent_project_list = json.loads(save_file.read())
            except JSONDecodeError:
                pass

        for index, project in enumerate(self.recent_project_list):
            self.recent_project_listbox.insert(index, project)

    def open_recent_project(self):
        "Open a recent project"
        selection = self.recent_project_listbox.curselection()

        if selection == ():
            print("No project selected!")
        else:
            print(self.recent_project_listbox.get(selection))

    def search_project(self):
        "Search a project in the file explorer"
        file_path = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a project file",
                                          filetypes = (("OpenCableHarness project files",
                                                        "*.OCH*"),
                                                       ("all files",
                                                        "*.*")))

        if file_path not in self.recent_project_list:
            self.recent_project_list.append(file_path)

            with open("recent_project.txt", 'w', encoding='utf-8') as save_file:
                save_file.write(json.dumps(self.recent_project_list))

        print(file_path)

    def create_project(self):
        "Create a new project"
        print(self.project_name_entry.get())
