#scp replaces png, you take the png, process it and send back rectangle coords, by that you replace txt file on rpi
import json
import torch
import math
import zmq

#get settings
with open("settings.json", "r") as file:
    settings = json.load(file)
rpiIP = settings['rpiIP']
txtFile = settings['txtFile']
PORT = settings['PORT']

# Format the data
#settings = json.dumps(settings, indent=2)

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')


def getData():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)  # Assuming PUSH-PULL communication
    socket.connect(f"tcp://{rpiIP}:{PORT}")
    socket.send(b"GetData")  # Send a message
    
    try:
        data = socket.recv()  # Wait for a message (will block)
        
        with open("output.png", "wb") as output:
            output.write(data)

    except zmq.error as e:
        print(f"ZMQ communication error: {e}")
        return None  # Or handle the error differently

    finally:
        socket.close()
        context.term()
    return data

def processFrame(frame):
    # Image
    im = frame

    # Inference
    results = model(im)

    # Filter person detections
    names = results.pandas().xyxy[0]['name'].tolist()
    person_indices = [i for i, name in enumerate(names) if name == 'person']

    # Extract and format x,y coordinates
    if person_indices:  # Check if any "person" detections exist
        person_xyxy = results.pandas().xyxy[0].iloc[person_indices].to_numpy()
        x_top = person_xyxy[:, 0].tolist()
        y_top = person_xyxy[:, 1].tolist()
        x_bottom = person_xyxy[:, 2].tolist()
        y_bottom = person_xyxy[:, 3].tolist()
        person_boxes = list(zip(x_top, y_top, x_bottom, y_bottom))  # Combine into list of tuples
    else:
        person_boxes = []  # Empty list if no "person" detections

    return person_boxes

def sendData(data):   
    #zmq init
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://{rpiIP}:{PORT}")
    socket.send(b"SendData")

    #get int coords (x-top,y-top,x-bottom,y-bottom)
    for lists in data:
        lists = list(lists)
        index = 0
        for item in lists:        
            if not (isinstance(item, int)):
                lists.remove(item)
                item = math.floor(item)
                lists.insert(index,item)
            index+=1
        socket.send_pyobj(lists)

    print("Sent data")
    #close socket
    socket.close()

#print settings
for i in settings:
    print(f"{i} -> {settings[i]}")

running = True
input = input("Take a look at the settings. Continue? (Y/n)")
if input == "n" or input == "N":
    running = False
while running:
    frame = getData()
    data = processFrame(frame)
    sendData(data)
    

    