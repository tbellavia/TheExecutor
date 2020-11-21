from .ConfigRunner import ConfigRunner
from .ConfigServer import ConfigServer
import yaml

class Config():
    def __init__(self, filename=None):
        self.runner = None
        self.server = None
        self.logpath = None

        if filename is not None:
            self.load(filename)
    
    def __repr__(self):
        runner = f"\"runner\" : {str(self.runner)}"
        server = f"\"server\" : {str(self.server)}"
        logpath = f"\"logpath\" : {self.logpath}"
        dump = f"{runner},\n{server},\n{logpath}"
        return f"<Config :\n{dump}\n>"

    def load(self, filename):
        with open(filename, "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        self.server = ConfigServer(data)
        self.runner = ConfigRunner(data)
        self.logpath = data['logs']['path']

        return self