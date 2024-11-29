"Main app"
from tkinter import ttk
import tkinter as tk

from settings import *
from graph import *
from components import *

root = tk.Tk()
root.config(width=800, height=600)

#Table
table_title_label = tk.Label(root, text="Creating cable")
table_title_label.grid(row=0, column=0)

cable_name_label = tk.Label(root, text="Cable name:")
cable_name_label.grid(row=1, column=0)

cable_name_entry = tk.Entry(root)
cable_name_entry.grid(row=1, column=1)

cable_color_label = tk.Label(root, text="Cable color:")
cable_color_label.grid(row=2, column=0)

cable_color_combobox = ttk.Combobox(values=["Black", "Red", "White", "Blue", "Green"])
cable_color_combobox.grid(row=2, column=1)

cable_gauge_label = tk.Label(root, text="Cable gauge (awg):")
cable_gauge_label.grid(row=3, column=0)

cable_gauge_combobox = ttk.Combobox(values=["14", "16", "18", "20", "22"])
cable_gauge_combobox.grid(row=3, column=1)

cable_list = []
def add_cable():
    for cable in cable_list:
        if cable.name is cable_name_entry.get():
            print("Name already in use!")
            return

    cable = Cable(cable_name_entry.get(), cable_color_combobox.get(), cable_gauge_combobox.get())

    cable_list.append(cable)
    cable_listbox.insert(len(cable_list), cable)

add_cable_button = tk.Button(root, text="Add cable", command=add_cable)
add_cable_button.grid(row=4, column=0, columnspan=2)

cables_label = tk.Label(root, text="Cables")
cables_label.grid(row=5, column=0, columnspan=2)

cable_listbox = tk.Listbox(root, width=40)
cable_listbox.grid(row=6, column=0, columnspan=2)

edit_cable_button = tk.Button(root, text="Edit cable")
edit_cable_button.grid(row=7, column=0, columnspan=2)

#Canvas
canvas = tk.Canvas(root, width=600, height=400,
                   borderwidth=0, highlightthickness=0, background="snow2")

canvas.grid(row=0, column=2, rowspan=8)

node_list = []

def create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

tk.Canvas.create_circle = create_circle

def create_node(event):
    x, y = event.x, event.y

    maxID = -1
    for node in node_list:
        maxID = max(maxID, node.ID)

    ID = maxID + 1
    node_list.append(Node(x, y, ID))

    canvas.create_circle(x, y, NODE_RADIUS, fill="SpringGreen3", tag=f"node{ID}")
    canvas.create_text(x, y, text=f"Node {ID}", tag=f"node{ID}")

def add_cable_to_node(node):
    selection = cable_listbox.curselection()

    if selection == ():
        print("No cable selected!")
    else:
        node.add(cable_listbox.get(cable_listbox.curselection()))
        print(node)

def delete_node(node):
    node_list.remove(node)
    canvas.delete(f"node{node.ID}")

menu_outside = tk.Menu(root, tearoff = 0)
menu_outside.add_command(label="Create new", command=create_node)


menu_inside = tk.Menu(root, tearoff = 0)

menu_inside.add_command(label="Add cable", command=add_cable_to_node)
menu_inside.add_separator()
menu_inside.add_command(label="Delete", command=delete_node)

def do_popup(event):
    "Make the menu appear"

    inside_node = inside_spacing = False
    clicked_node = Node(-1, -1, -1)
    for node in node_list:
        if node.is_inside_node(event.x, event.y):
            inside_node = True
            clicked_node = node

        if node.is_inside_spacing(event.x, event.y):
            inside_spacing = True

    if inside_node:
        menu_inside.entryconfig(0, command=lambda: add_cable_to_node(clicked_node))
        menu_inside.entryconfig(2, command=lambda: delete_node(clicked_node))
        try:
            menu_inside.tk_popup(event.x_root, event.y_root)
        finally:
            menu_inside.grab_release()

    if not inside_spacing:
        menu_outside.entryconfig(0, command=lambda: create_node(event))
        try:
            menu_outside.tk_popup(event.x_root, event.y_root)
        finally:
            menu_outside.grab_release()

root.title("Open Cable Harness")
root.bind("<Button-3>", do_popup)

root.mainloop()
