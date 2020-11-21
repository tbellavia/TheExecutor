import json

class ConfigRunner():
    def __init__(self, data=None):
        self.timeout = None
        self.resources_path = None
        self.snippets_path = None

        if data is not None:
            self.load(data)

    def __repr__(self):
        return f"<ConfigRunner : .timeout = {self.timeout}, .resources_path = {self.resources_path}, .snippets_path = {self.snippets_path}>"

    def __str__(self):
        return json.dumps(self.__dict__, sort_keys=True, indent=4)

    def load(self, data):
        runner = data['runner']

        self.timeout = runner['process']['timeout']
        self.resources_path = runner['resources']['path']
        self.snippets_path = runner['snippets']['path']