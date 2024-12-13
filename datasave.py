"Save data list as json and load them"
import os

import json
from json.decoder import JSONDecodeError

class DataSave:
    "SaveFile object : a var that can be saved into a file"
    data_path = "data/"

    slots = dict()
    data = dict(dict())

    def __init__(self, file_name, slots):
        self.file_name = file_name
        self.slots = slots

        self.data = self.load()

        if self.data == dict():
            for slot in slots:
                self.data[slot] = dict()

    def __getitem__(self, slot):
        return self.data.get(slot)

    def get_path(self):
        "Return path from file name"

        return DataSave.data_path + self.file_name

    def get_list(self, slot):
        "Return a list of the names"

        return [key for key in self.data.get(slot)]

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

    def update(self, slot, name, updated_data):
        "Replace everything in the save file to update the data dict"

        #Error check
        if slot not in self.slots:
            raise SyntaxError()

        #Check data integrity
        if name == "":
            return "Name cannot be empty!"
        if name in self.data[slot]:
            return "Name already exists!"

        #Update data
        self.data[slot][name] = updated_data

        self.rewrite_save_file()

        return ""

    def remove(self, slot, name):
        "Update the save list of recent projects to save file"
        del self.data[slot][name]

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
