"Save data dict as json and load them"
import os

import json
from json.decoder import JSONDecodeError

class DataSave:
    "Save file with tags"

    data_path = "data/"
    data = dict()

    def __init__(self, file_name):
        self.file_name = file_name
        self.data = self.load()

    def __getitem__(self, keys):
        return self.get_item(self.get_tag(keys))

    def __setitem__(self, keys, new_data):
        self.set_item(self.get_tag(keys), new_data)

    def __delitem__(self, keys):
        self.del_item(self.get_tag(keys))

    def get_item(self, tag):
        "Get dictionnary item"
        return self.data.get(tag)

    def set_item(self, tag, new_value):
        "Set dictionnary item"
        self.data[tag] = new_value

        self.rewrite_save_file()

    def del_item(self, tag):
        "Delete dictionnary item"
        del self.data[tag]

        self.rewrite_save_file()

    def check_tag_integrity(self, tag):
        "Check tag integrity"

        if tag[-1] == "_":
            return "Name cannot be empty!"
        if self.get_item(tag):
            return "Name already exist!"

        return ""

    def get_tag(self, keys):
        "Turn a tuple to a dictionary tag"

        if isinstance(keys, tuple):
            return "_".join(keys)
        else:
            return keys

    def get_path(self):
        "Return path from file name"

        return DataSave.data_path + self.file_name

    def get_children(self, prefix_tag):
        "Return a list of the tags"
        children = list()
        prefix_tag = prefix_tag + "_"

        for tag in self.data.keys():
            if tag.startswith(prefix_tag):
                children.append(tag.removeprefix(prefix_tag))

        return children

    def load(self):
        """Load recent projects from the save file"""
        try:
            with open(self.get_path(), 'r', encoding='utf-8') as save_file:
                try:
                    return json.loads(save_file.read())
                except JSONDecodeError:
                    return dict()
        except FileNotFoundError:
            return dict()

    def remove(self, key):
        "Update the save list of recent projects to save file"
        del self.data[key]

        self.rewrite_save_file()

    def rewrite_save_file(self):
        "Update everything in the save file"

        try:
            with open(self.get_path(), 'w', encoding='utf-8') as file:
                file.write(json.dumps(self.data))
        except FileNotFoundError:
            try:
                os.mkdir("data")
            except FileExistsError:
                pass

            try:
                os.mkdir("data/projects")
            except FileExistsError:
                pass

            with open(self.get_path(), 'w', encoding='utf-8') as file:
                file.write(json.dumps(self.data))
