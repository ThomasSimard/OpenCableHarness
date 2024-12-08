"Cable class"

class Cable:
    "Class representing a cable"
    name = ""
    color = ""
    gauge = ""

    def __init__(self, name, color, gauge):
        self.name = name
        self.color = color
        self.gauge = gauge

    def __str__(self):
        return f"Cable : {self.name}, color : {self.color}, {self.gauge} awg"

class Connector:
    "Class representing a connector"
    name = ""
    number_of_pins = 0

    def __init__(self, name, number_of_pins):
        self.name = name
        self.name = number_of_pins
