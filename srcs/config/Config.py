from .ConfigRunner import ConfigRunner
from .ConfigServer import ConfigServer
import yaml


class Config:
    def __init__(self, filename=None):
        self.runner = None
        self.server = None
        self.log_path = None

        if filename is not None:
            self.load(filename)
    
    def __repr__(self):
        runner = f"\"runner\" : {str(self.runner)}"
        server = f"\"server\" : {str(self.server)}"
        log_path = f"\"log_path\" : {self.log_path}"
        dump = f"{runner},\n{server},\n{log_path}"
        return f"<Config :\n{dump}\n>"

    def load(self, filename):
        with open(filename, "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        self.server = ConfigServer(data)
        self.runner = ConfigRunner(data)
        self.log_path = data['logs']['path']

        return self
