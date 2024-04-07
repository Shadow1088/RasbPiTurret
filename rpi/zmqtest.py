import zmq
import json

port = "5555"

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(f"tcp://*:{port}")

while True:
    message = socket.recv()
    
    if message == b"GetData":
        data = ["12354"]
        data_string = json.dumps(data)
        socket.send(data_string.encode())
    else:
        print("unkown message receiver:", message)
    
socket.close()
context.term()