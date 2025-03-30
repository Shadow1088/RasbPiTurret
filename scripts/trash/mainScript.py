import cv2
import RPi.GPIO as GPIO
import time
import zmq
import math

try:
    #Video size
    width = 320 #px
    height = 240
    #Count fps
    start_time = 0
    frames_processed = 0

    #cameras index (in case you have multiple cameras, replace it with correct index)
    cap = cv2.VideoCapture(0)

    #OPENCV
    #####################x
    #####################x
    #SERVO

    servo_piny = 18
    servo_pinx = 16


    GPIO.setmode(GPIO.BCM)

    GPIO.setup(servo_piny, GPIO.OUT)
    GPIO.setup(servo_pinx, GPIO.OUT)

    servoy_min = 100 #degrees, UP
    servoy_max = 180 #degrees, DOWN
    servoy_mid = 140 # degrees, MID // 135

    servoy = GPIO.PWM(servo_piny,50)
    servox = GPIO.PWM(servo_pinx,50)
    servoy.start(0)
    servox.start(0)

    def setAngle(servo, angle, sleep):
        if sleep==0:
            sleep=0.5
        if servo == servoy:
            servoy.ChangeDutyCycle(2+(angle/18))
            time.sleep(sleep)
            servoy.ChangeDutyCycle(0)
        elif servo == servox:
            servox.ChangeDutyCycle(2+(angle/18))
            time.sleep(sleep)
            servox.ChangeDutyCycle(0)
        else:
            print("[ ! ] --> setAngle function error")

    setAngle(servoy,140,0)
    currenty=140
    setAngle(servox,90,0)
    currentx=90

    last_seen = time.time()
    left=True
    def searching(mode,sleep):
        global currentx
        global currenty
        
        if mode == 0:
            #if currentx >= 5:
            currentx = currentx - 5
            setAngle(servox,currentx,sleep)
            setAngle(servoy,135,sleep)
        elif mode == 1:
            currentx+=5
            setAngle(servox,currentx,sleep)
            setAngle(servoy,100,sleep)

    #################################################x
    #################################################x
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

    ######################################################x
    ######################################################x

    running = True
    while running:
        # capture a frame (ret is return value, its a boolean that says if its all good or nah)
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Unable to capture the frame!")
            break


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

        x_lsr = 160
        y_lsr = 120
        
        
        if cv2.waitKey(1) == ord("q"):
            break
        if person != []:
            bounding_xtop = math.floor(person[0]*0.4)
            bounding_ytop = math.floor(person[1]*0.4)
            bounding_xbottom = math.floor(person[2]*0.6)
            bounding_ybottom = math.floor(person[3]*0.6)
            
            face_width = bounding_xbottom - bounding_xtop
            face_height = bounding_ybottom - bounding_ytop

            is_center = (bounding_xtop < x_lsr < bounding_xbottom) and (bounding_ytop < y_lsr < bounding_ybottom)
            
        
            if ((face_width // 2)+bounding_xbottom) < x_lsr and is_center != True: 
                currentx+=2
                setAngle(servox, currentx,0.25)
                
            if ((face_height // 2)+bounding_ybottom) < y_lsr and is_center != True: 
                currenty-=2
                setAngle(servoy, currenty,0.25)

            if ((face_width // 2)+bounding_xbottom) > x_lsr and is_center != True: 
                currentx-=2
                setAngle(servox, currentx,0.25)
                
            if ((face_height // 2)+bounding_ybottom) > y_lsr and is_center != True: 
                currenty+=2
                setAngle(servoy, currenty,0.25)

            if currentx >= 180:
                print("[!] --> X is at 180 degrees, cant rotate no more!")
            if currenty >= 180:
                print("[!] --> Y is at 180 degrees, cant rotate no more!")
            if currentx <= 0:
                print("[!] --> X is at 0 degrees, cant rotate no more!")
            if currenty <= 100:
                print("[!] --> Y is at 100 degrees, cant rotate no more!")
            print(person)
            print(f"X: {currentx}")
            print(f"Y: {currenty}")
                
            cv2.rectangle(frame, (person[0], person[1]), (face_width, face_height), (4,247,13), 2)

        cv2.imshow("camera-output+detection", frame)

        if elapsed_time > 1:
            fps = frames_processed / elapsed_time
            print(f"FPS: {fps:.2f}")
            #reset
            start_time = current_time
            frames_processed = 0
        
        # check it out (later put the logic for processing the frames here)
             
        

except cv2.error:
    print(cv2.error)
finally:
    # release MEE
    socket.close()
    context.term()
    cap.release()
    cv2.destroyAllWindows()
    servoy.stop()
    servox.stop()
    GPIO.cleanup()
