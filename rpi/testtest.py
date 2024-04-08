import zmq
import time
import cv2


#sizes
width = 320 #px
height = 240
# count fps
start_time = 0
frames_processed = 0
#cameras index (in case you have multiple cameras, replace it with correct index)
cap = cv2.VideoCapture(0)

#OPENCV
#####################x
#ZMQ
port = "5555"
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(f"tcp://*:{port}")

def getMessage():
    global socket
    print("Getting message")
    message = socket.recv()
    print(f"Message: {message}")
    return message


def sendData(frame, port):
    global socket
    print("Sending data")
    socket.send(frame.tobytes())
    print(f"Sent data")

def receiveData():
    global socket
    print("Receiving data")
    data = socket.recv_pyobj()
    print(f"Received data: {data}")

running = True
while running:
    #capture a frame (ret is return value, its a boolean that says if its all good or nah)
    ret, frame = cap.read()
    
    #resize
    if ret:
        frame = cv2.resize(frame, (width, height))
    
    frames_processed +=1
    current_time = time.time()
    elapsed_time = current_time - start_time
    
    message = getMessage()
    if message == "b'getData'":
        sendData(frame, "5555")
    elif message == "b'sendData'":
        people = receiveData()

    if ret:
        cv2.imshow("camera-output+detection", frame)
        
        if cv2.waitKey(1) == ord("q"):
            break
        
    else:
        print("Error: Unable to capture the frame!")
        break

# release MEE
socket.close()
context.term()
cap.release()
cv2.destroyAllWindows()
