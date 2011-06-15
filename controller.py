import json
import socket

numPlayers = 6

mapPath = "map.json"
f = open(mapPath, 'r')
mapData = json.load(f)

AIs = [6125 .. 6130]



HOST = '127.0.0.1'    # The remote host
PORT = 6125              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send('Hello, world2')
data = s.recv(1024)
s.close()
print 'Received', repr(data)
