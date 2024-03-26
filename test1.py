import cv2 as cv
import RPi.GPIO as GPIO
import time

#sizes
width = 320 #px
height = 240
# count fps
start_time = 0
frames_processed = 0

#cameras index (in case you have multiple cameras, replace it with correct index)
#video_path = "title-artist2.mp4"
cap = cv.VideoCapture(0)

# what "module" (cascade classifier) to choose?
#   "haarcascade_frontalface_default.xml" - face detection,
#   "haarcascade_fullbody.xml" - full body detection
#	"haarcascade_upperbody.xml" - upper body detection
cascade_classifier = cv.CascadeClassifier("haarcascade_frontalface_default.xml")

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


running = True
while running:
    # capture a frame (ret is return value, its a boolean that says if its all good or nah)
    ret, frame = cap.read()
    
    #resize
    if ret:
        frame = cv.resize(frame, (width, height))
    
    frames_processed +=1
    current_time = time.time()
    elapsed_time = current_time - start_time
    
    # Convert frame into grayscale (Haar Cascades work better in grayscale)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    # Detect people
    people = cascade_classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    
    # Draw rectangle around people
    for (x, y, w, h) in people:
        test = cv.rectangle(frame, (x, y), (x+w, y+h), (4,247,13), 2)  # cooloring is not RGB but BGR...
    
    # Draw + (can remove later, helps servo debug)
    frame_height, frame_width = frame.shape[:2]
    symbol_width = frame_width // 10
    symbol_height =  frame_height // 10
    center_x = frame_width // 2
    center_y = frame_height // 2
    half_lenght = symbol_height // 2
    top_line_start = (center_x, center_y - half_lenght)
    top_line_end = (center_x, center_y + half_lenght)
    bottom_line_start = (center_x - half_lenght, center_y)
    bottom_line_end = (center_x + half_lenght, center_y)
    cv.line(frame, top_line_start, top_line_end, (0,0,255), 1)
    cv.line(frame, bottom_line_start, bottom_line_end, (0,0,255), 1)
    
    try:
        #is center in rectangle
        face_x, face_y, face_width, face_height = people[0]   
        
        is_center = (face_x < center_x < (face_x+face_width) and face_y < center_y <(face_y+face_height))
        #print(is_center)
        #rotate X if upperleft
        if face_x + face_width // 2 < center_x and is_center != True: #180degrees = left
            currentx = currentx+5
            setAngle(servox,currentx,0.4)
        #rotate X if upperright
        elif face_x + face_width // 2 > center_x and is_center != True:
            currentx = currentx-5
            setAngle(servox,currentx,0.4)
        #rotate Y if lowerleft
        if face_y + face_width // 2 < center_y and is_center != True: #180degrees = right
            currenty = currenty-5
            setAngle(servoy,currenty,0.4)
        elif face_y + face_width // 2 > center_y and is_center != True:
            currenty = currenty+5
            setAngle(servoy,currenty,0.4)
        last_seen = time.time()
                        
    except:
        if (time.time() - last_seen) > 5:
            print("[!] --> dont see anyone, looking for people..!")
            if left:
                if currentx<=5:
                    left=False
                    continue
                searching(0,0.4)
            else:
                if currentx>170:
                    left=True
                searching(1,0.4)
    
    if currentx >= 180:
        currentx = 180
        print("[!] --> X is at 180 degrees, cant rotate no more!")
    if currenty >= 180:
        currenty = 180
        print("[!] --> Y is at 180 degrees, cant rotate no more!")
    if currentx <= 0:
        currentx = 0
        print("[!] --> X is at 0 degrees, cant rotate no more!")
    if currenty <= 100:
        currenty = 100
        print("[!] --> Y is at 100 degrees, cant rotate no more!")
    



    if elapsed_time > 1:
        fps = frames_processed / elapsed_time
        print(f"FPS: {fps:.2f}")
        #reset
        start_time = current_time
        frames_processed = 0
    
    # check it out (later put the logic for processing the frames here)
    if ret:
        cv.imshow("camera-output+detection", frame)
        
        if cv.waitKey(1) == ord("q"):
            break
        
    else:
        print("Error: Unable to capture the frame!")
        break
    
# release MEE
cap.release()
cv.destroyAllWindows()
servoy.stop()
servox.stop()
GPIO.cleanup()
