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
    node = None
    number_of_pins = 0

    def __init__(self, node):
        self.node = node
