import cv2 as cv
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
cascade_classifier = cv.CascadeClassifier("haarcascade_frontalface_default.xml")

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
        cv.rectangle(frame, (x, y), (x+w, y+h), (4,247,13), 2)  # cooloring is not RGB but BGR...
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