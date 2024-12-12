"Save data list as json and load them"
import json
from json.decoder import JSONDecodeError

class SaveFile:
    "SaveFile object : a var that can be saved into a file"
    data_path = "data/"

    class Data:
        "Check data validity"
        data_dict = dict()

        def __init__(self, data, save):
            self.data_dict = data
            self.save = save

        def add(self, name, data):
            "Add data to the dict with checks"

            if name == "":
                return "Name cannot be empty!"
            elif name in self.data_dict:
                return "Name already exists!"
            else:
                self.data_dict.update({name: data})
                self.save()

            return ""

        def remove(self, name):
            "Remove data to the dict"

            del self.data_dict[name]
            self.save()

    def __init__(self, file_name):
        self.file_name = file_name
        self.data = self.load()

    def get_path(self):
        "Return path from file name"

        return "data/" + self.file_name

    def load(self):
        """Load recent projects from the save file"""
        try:
            with open(self.get_path(), 'r', encoding='utf-8') as save_file:
                try:
                    return json.loads(save_file.read())
                except JSONDecodeError:
                    return []
        except FileNotFoundError:
            return []

    def replace(self, new_data):
        "Replace everything in the save file"

        self.data = new_data

        with open(self.get_path(), 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.data))

    def append(self, new_data):
        "Update the save list of recent projects to save file"

        if new_data not in self.data:
            self.data.append(new_data)

            with open(self.get_path(), 'w', encoding='utf-8') as file:
                file.write(json.dumps(self.data))

            return True

        return False

    def remove(self, remove_data):
        "Update the save list of recent projects to save file"

        if remove_data in self.data:
            self.data.remove(remove_data)

            with open(self.get_path(), 'w', encoding='utf-8') as file:
                file.write(json.dumps(self.data))

            return True

        return False
