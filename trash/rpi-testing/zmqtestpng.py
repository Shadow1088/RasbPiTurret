import zmq
import json

port = "5555"
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(f"tcp://*:{port}")

while True:
    message = socket.recv()
    
    if message == b"GetData":
        with open("frame.png", "rb") as file:
            data = file.read()
        socket.send(data)
    else:
        print("unkown message receiver:", message)
    
    
socket.close()
context.term()