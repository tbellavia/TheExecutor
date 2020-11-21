import json

class ConfigServer():
    def __init__(self, data=None):
        self.token = None
        self.channels = None
        self.members = None
        self.roles = None

        if data is not None:
            self.load(data)

    def __repr__(self):
        return f"<ConfigServer : .token = {self.token}, .channels = {self.channels}, .members = {self.members}, .roles = {self.roles}>"
    
    def __str__(self):
        return json.dumps(self.__dict__, sort_keys=True, indent=4)

    def load(self, data):
        server = data['server']
        scope = server['scope']

        self.token = server['token']
        self.channels = scope['channels']
        self.roles = scope['roles']
        self.members = scope['members']