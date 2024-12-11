"Cable class"

import json

class Wire:
    "Class representing a wire"
    name = ""
    color = ""
    gauge = ""

    def __init__(self, name, color, gauge):
        self.name = name
        self.color = color
        self.gauge = gauge

    def to_json(self):
        "Put the object in json format"
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)

    def __str__(self):
        return f"Wire : {self.name}, color : {self.color}, {self.gauge} awg"

class Connector:
    "Class representing a connector"
    name = ""
    number_of_pins = 0

    def __init__(self, name, number_of_pins):
        self.name = name
        self.name = number_of_pins
