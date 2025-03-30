import zmq
import json

def getData(IP, PORT):
    host = f"tcp://{IP}:{PORT}"

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(host)
    socket.send(b"GetData")
    
    message = socket.recv().decode()
    data = json.loads(message)
    
    socket.close()
    context.term()
    return data
    
getData("192.168.0.102", "5555")