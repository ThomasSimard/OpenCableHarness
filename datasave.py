"Save data dict as json and load them"
import os

import json
from json.decoder import JSONDecodeError

class DataSave:
    "Save file with tags"

    data_path = "data/"
    data: dict = dict()

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.data = self.load()

    def __getitem__(self, keys: tuple[str, ...]):
        return self.get_item(self.get_tag(keys))

    def __setitem__(self, keys: tuple[str, ...], new_data) -> None:
        self.set_item(self.get_tag(keys), new_data)

    def __delitem__(self, keys: tuple[str, ...]) -> None:
        self.del_item(self.get_tag(keys))

    def get_item(self, tag: str):
        "Get dictionnary item"
        return self.data.get(tag)

    def set_item(self, tag: str, new_value) -> None:
        "Set dictionnary item"
        self.data[tag] = new_value

        self.rewrite_save_file()

    def del_item(self, tag: str) -> None:
        "Delete dictionnary item"
        del self.data[tag]

        self.rewrite_save_file()

    def check_tag_integrity(self, tag: str) -> str:
        "Check tag integrity"

        if tag[-1] == "_":
            return "Name cannot be empty!"
        if self.get_item(tag):
            return "Name already exist!"

        return ""

    def get_tag(self, keys: tuple[str, ...]) -> str:
        "Example: ('val_x', 'val_y') -> 'x_y'"

        if isinstance(keys, tuple):
            return "_".join(keys)
        else:
            return keys

    def get_path(self) -> str:
        "Return path from file name"

        return DataSave.data_path + self.file_name

    def get_children(self, prefix_tag: str) -> list[str]:
        "Return a list of the tags"
        children = list()
        prefix_tag = prefix_tag + "_"

        for tag in self.data.keys():
            if tag.startswith(prefix_tag):
                children.append(tag.removeprefix(prefix_tag))

        return children

    def load(self) -> dict:
        """Load recent projects from the save file"""
        try:
            with open(self.get_path(), 'r', encoding='utf-8') as save_file:
                try:
                    return json.loads(save_file.read())
                except JSONDecodeError:
                    return dict()
        except FileNotFoundError:
            return dict()

    def rewrite_save_file(self) -> None:
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
