import cv2 as cv

#cameras index (in case you have multiple cameras, replace it with correct index)
cap = cv.VideoCapture(0)

running = True
while running:
    # capture a frame (ret is return value, its a boolean that says if its all good or nah)
    ret, frame = cap.read()
    
    # check it out (later put the logic for processing the frames here)
    if ret:
        cv.imshow("camera", frame)
        
        if cv.waitKey(1) == ord("q"):
            break
        
    else:
        print("Error: Unable to capture the frame!")
        break
    
# release MEE
cap.release()
cv.destroyAllWindows()        
    