class Connections:

    def __init__(self, servers):
        self.servers = servers

class Server:

    def __init__(self, uri, label):
        self.uri = uri
        self.logins = []
        self.label = label

class Login:

    def __init__(self, username, password):
        self.username = username
        self.password = password
