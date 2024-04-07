import zmq
import cv2
import numpy as np
import time

def getData(IP, PORT):
    host = f"tcp://{IP}:{PORT}"

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(host)
    socket.send(b"GetData")
    
    data = socket.recv()

    # Decode the received image data (assuming PNG format)
    frame = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)

    cv2.imshow('Processed Frame', frame)
    cv2.waitKey(0)

    cv2.destroyAllWindows()

    with open("output.png", "wb") as f:
        f.write(data)

    socket.close()
    context.term()
    return data

getData("192.168.0.105", "5555")

