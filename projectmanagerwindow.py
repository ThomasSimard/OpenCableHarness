"""Project manager window"""

from tkinter import ttk
from tkinter import filedialog
import tkinter as tk

import json
from json.decoder import JSONDecodeError

import pathlib

from projectwindow import ProjectWindow

class ProjectManagerWindow:
    """Let the user create and open projects"""

    def __init__(self, root):
        self.root = root

        self.project_file_path = ""
        self.project_directory_path = f"{pathlib.Path().resolve()}\projects"

        recent_project_label = tk.Label(root, text="Recent project:")
        recent_project_label.grid(row=0, column=0)

        self.recent_project_listbox = tk.Listbox(root, width=80)
        self.recent_project_listbox.grid(row=1, column=0, columnspan=2, padx=20, pady=20)

        self.recent_project_list = []
        self.load_recent_project()

        open_recent_project_button = tk.Button(root, text="Open recent project",
            command=self.open_recent_project)

        open_recent_project_button.grid(row=2, column=0, columnspan=2)

        search_project_button = tk.Button(root, text="Search project file",
            command=self.search_project)

        search_project_button.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

        separator = ttk.Separator(root, orient='horizontal')
        separator.grid(row=4, column=0, columnspan=2, sticky="ew")

        create_project_label = tk.Label(root, text="Create project")
        create_project_label.grid(row=5, column=0, columnspan=2)

        project_name_label = tk.Label(root, text="Project name:")
        project_name_label.grid(row=7, column=0)

        self.project_name_entry = tk.Entry(root)
        self.project_name_entry.grid(row=7, column=1)

        new_project_button = tk.Button(root, text="Create new project",
            command=self.create_project)

        new_project_button.grid(row=8, column=0, columnspan=2, padx=20, pady=20)

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
            self.project_file_path = self.recent_project_listbox.get(selection)
            self.open_project_tab()

    def update_recent_project(self):
        "Update the save list of recent projects"

        if self.project_file_path not in self.recent_project_list:
            self.recent_project_list.append(self.project_file_path)

            with open("recent_project.txt", 'w', encoding='utf-8') as save_file:
                save_file.write(json.dumps(self.recent_project_list))

            self.recent_project_listbox.delete(0, len(self.recent_project_list))
            self.load_recent_project()

    def search_project(self):
        "Search a project in the file explorer"
        self.project_file_path = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a project file",
                                          filetypes = (("OpenCableHarness project files",
                                                        "*.OCH*"),
                                                       ("all files",
                                                        "*.*")))

        self.update_recent_project()
        self.open_project_tab()

    def create_project(self):
        "Create a new project"
        self.project_file_path = f"{self.project_directory_path}\{self.project_name_entry.get()}.OCH"

        self.update_recent_project()
        self.open_project_tab()

    def get_project_name(self):
        "Get the project name from the path"

        return self.project_file_path.split("\\")[-1]

    def open_project_tab(self):
        "Once a project is created or opened, open it in a new tab"

        project_tab_frame = ttk.Frame(self.root.master)

        ProjectWindow(project_tab_frame)

        self.root.master.add(project_tab_frame, text=self.get_project_name())
        self.root.master.select(self.root.master.index("end") - 1)
