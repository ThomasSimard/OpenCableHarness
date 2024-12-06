"Main app"
from tkinter import ttk
import tkinter as tk

from projectmanagerwindow import ProjectManagerWindow

def main():
    "Main fonction of the app"

    root = tk.Tk()
    root.config(width=800, height=600)
    root.title("Open Cable Harness")

    tab_manager = ttk.Notebook(root)

    project_manager_tab_frame = ttk.Frame(tab_manager)

    ProjectManagerWindow(project_manager_tab_frame)

    tab_manager.add(project_manager_tab_frame, text ='Project manager')
    tab_manager.grid(row=0)

    root.mainloop()

if __name__ == '__main__':
    main()
