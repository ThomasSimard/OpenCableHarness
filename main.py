"Main app"
from tkinter import ttk
import tkinter as tk

from projectmanager import ProjectWindow

from settings import *
from graph import *
from components import *

def create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

class MainWindow:
    cable_list = []
    node_list = []

    def __init__(self, root):
        self.Table(root)
        self.Canvas(root)

    def Canvas(self, root):
        self.canvas = tk.Canvas(root, width=800, height=600,
                        borderwidth=0, highlightthickness=0, background="snow2")

        self.canvas.grid(row=0, column=2, rowspan=8)

        tk.Canvas.create_circle = create_circle

        self.menu_outside = tk.Menu(root, tearoff = 0)
        self.menu_outside.add_command(label="Create new", command=self.create_node)


        self.menu_inside = tk.Menu(root, tearoff = 0)

        self.menu_inside.add_command(label="Add cable", command=self.add_cable_to_node)
        self.menu_inside.add_separator()
        self.menu_inside.add_command(label="Delete", command=self.delete_node)

        self.node_label = tk.Label(text="Nodes")
        self.node_label.grid(row=8, column=0, columnspan=2)

        self.node_listbox = tk.Listbox(root, width=40)
        self.node_listbox.grid(row=9, column=0, columnspan=2)

    def Table(self, root):
        self.title_label = tk.Label(root, text="Creating cable")
        self.title_label.grid(row=0, column=0)

        self.cable_name_label = tk.Label(root, text="Cable name:")
        self.cable_name_label.grid(row=1, column=0)

        self.cable_name_entry = tk.Entry(root)
        self.cable_name_entry.grid(row=1, column=1)

        self.cable_color_label = tk.Label(root, text="Cable color:")
        self.cable_color_label.grid(row=2, column=0)

        self.cable_color_combobox = ttk.Combobox(values=["Black", "Red", "White", "Blue", "Green"])
        self.cable_color_combobox.grid(row=2, column=1)

        self.cable_gauge_label = tk.Label(root, text="Cable gauge (awg):")
        self.cable_gauge_label.grid(row=3, column=0)

        self.cable_gauge_combobox = ttk.Combobox(values=["14", "16", "18", "20", "22"])
        self.cable_gauge_combobox.grid(row=3, column=1)

        self.add_cable_button = tk.Button(root, text="Add cable", command=self.add_cable)
        self.add_cable_button.grid(row=4, column=0, columnspan=2)

        self.cables_label = tk.Label(root, text="Cables")
        self.cables_label.grid(row=5, column=0, columnspan=2)

        self.cable_listbox = tk.Listbox(root, width=40)
        self.cable_listbox.grid(row=6, column=0, columnspan=2)

        self.edit_cable_button = tk.Button(root, text="Edit cable")
        self.edit_cable_button.grid(row=7, column=0, columnspan=2)

    def add_cable(self):
        for cable in self.cable_list:
            if cable.name is self.cable_name_entry.get():
                print("Name already in use!")
                return

        cable = Cable(self.cable_name_entry.get(), self.cable_color_combobox.get(), self.cable_gauge_combobox.get())

        self.cable_list.append(cable)
        self.cable_listbox.insert(len(self.cable_list), cable)

    def create_node(self, event):
        x, y = event.x, event.y

        maxID = -1
        for node in self.node_list:
            maxID = max(maxID, node.tag)

        tag = maxID + 1
        node = Node(x, y, tag)

        self.node_list.append(node)
        self.node_listbox.insert(tag, node)

        self.canvas.create_circle(x, y, NODE_RADIUS, fill="SpringGreen3", tag=f"node{tag}")
        self.canvas.create_text(x, y, text=f"Node {tag}", tag=f"node{tag}")

    def add_cable_to_node(self, node):
        selection = self.cable_listbox.curselection()

        if selection == ():
            print("No cable selected!")
        else:
            node.add(self.cable_listbox.get(selection))
            print(node)

    def delete_node(self, node):
        self.node_list.remove(node)
        self.node_listbox.delete(node.tag)

        self.canvas.delete(f"node{node.tag}")

    def do_popup(self, event):
        "Make the menu appear"

        inside_node = inside_spacing = False
        clicked_node = Node(-1, -1, -1)
        for node in self.node_list:
            if node.is_inside_node(event.x, event.y):
                inside_node = True
                clicked_node = node

            if node.is_inside_spacing(event.x, event.y):
                inside_spacing = True

        if inside_node:
            self.menu_inside.entryconfig(0, command=lambda: self.add_cable_to_node(clicked_node))
            self.menu_inside.entryconfig(2, command=lambda: self.delete_node(clicked_node))
            try:
                self.menu_inside.tk_popup(event.x_root, event.y_root)
            finally:
                self.menu_inside.grab_release()

        if not inside_spacing:
            self.menu_outside.entryconfig(0, command=lambda: self.create_node(event))
            try:
                self.menu_outside.tk_popup(event.x_root, event.y_root)
            finally:
                self.menu_outside.grab_release()


def main():
    root = tk.Tk()
    root.config(width=800, height=600)
    root.title("Open Cable Harness")

    main_window = ProjectWindow(root)

    #root.bind("<Button-3>", main_window.do_popup)

    root.mainloop()

if __name__ == '__main__':
    main()
