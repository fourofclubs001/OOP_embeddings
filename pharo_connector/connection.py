import socket
import json
import time

instructionsToPerform = [
    {
        "variable": "var",
        "receiver": "OrderedCollection",
        "selector": "new",
        "arguments": []
    },
    {
        "variable": "var2",
        "receiver": "OrderedCollection",
        "selector": "new",
        "arguments": []

    },
    {
        "variable": "var3",
        "receiver": "var",
        "selector": "add:",
        "arguments": [1]
    }
]
responses = []

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1',9290))
client.settimeout(10)
for instruction in instructionsToPerform:
    time.sleep(0.1)
    message = json.dumps(instruction)
    print(message)
    data = (message+ '\n').encode("utf-8")
    client.sendall(data)
    response = json.dumps(client.recv(5000).decode('utf-8'))
    responses.append(response)
    print(response)
client.shutdown(socket.SHUT_RDWR)
client.close()