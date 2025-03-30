import zmq
import time
import cv2
import math

try:
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

        socket.send_pyobj(frame)
        print(f"Sent data")

    def receiveData():
        global socket
        response = socket.send(b"receiving")
        print("Receiving data")
        data = socket.recv_pyobj()
        print(f"Received data: ")
        response2 = socket.send(b"SUCCESS")
        return data
        

    

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
        if message == b'getData':
            sendData(frame, "5555")
        elif message == b'sendData':
            data = receiveData()
        
        #get x-top, y-top, x-bottom, y-bottom from one person
        person = []
        for i in data:
            for j in i:
                person.append(math.floor(j))
        print(person)
        

        if ret:
            cv2.imshow("camera-output+detection", frame)
            #cv2.rectangle(frame, (person[0],person[1]),(person[2],person[3]),(255,0,0),2)
            if cv2.waitKey(1) == ord("q"):
                break
        else:
            print("Error: Unable to capture the frame!")
            break
except:
    pass
finally:
    # release MEE
    socket.close()
    context.term()
    cap.release()
    cv2.destroyAllWindows()

