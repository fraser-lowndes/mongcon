from jsonpickle import encode as json_encode, decode as json_decode
from models import *
import subprocess, shlex

file_location = './connections.mongocon'

if open:
    pass

file_contents = None

def read_connections_file():
    with open(file_location, 'r') as file:
        return file.read()

def write_empty_schema():
    with open(file_location, 'w') as file:
        file.write(json_encode(Connections(servers=[Server(uri='mongodb://localhost:27017', label='local')]), unpicklable=False))
        file.flush()

try:
    file_contents = read_connections_file()
    if not len(file_contents):
        write_empty_schema()
except FileNotFoundError:
    write_empty_schema()
    file_contents = read_connections_file()

servers = [ Server(uri=server['uri'],
                   label=server['label']) for server in json_decode(file_contents)['servers'] ]

connections = Connections(servers=servers)

servers = '\n'.join([ f'{server.label} ({server.uri})' for server in connections.servers ])
print(f'servers: \n{servers}')

conn_to_uri = None

while not conn_to_uri:
    conn_to = input('connect to: ')
    servers = [ server for server in connections.servers if server.label == conn_to ]

    if not servers:
        print(f'not known: {conn_to}')
    else:
        conn_to_uri = servers[0].uri

mongo_cmd = f'mongo "{conn_to_uri}"'

subprocess.Popen(shlex.split(mongo_cmd), shell=True).wait()

