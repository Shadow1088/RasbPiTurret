import cv2 as cv

import time

#sizes
width = 320 #px
height = 240
# count fps
start_time = 0
frames_processed = 0

#cameras index (in case you have multiple cameras, replace it with correct index)
cap = cv.VideoCapture(0)

#OPENCV
#####################x
#####################x

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
    
    try:
        pass
                        
    except:
        print("[!] --> dont see anyone, looking for people..!")

   

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

