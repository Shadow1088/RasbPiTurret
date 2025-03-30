import torch
import math

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

while True:
    # Image
    im = 'https://ultralytics.com/images/zidane.jpg'

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

    #get int coords (x-top,y-top,x-bottom,y-bottom)
    for lists in person_boxes:
        lists = list(lists)
        index = 0
        for item in lists:        
            if not (isinstance(item, int)):
                lists.remove(item)
                item = math.floor(item)
                lists.insert(index,item)
            index+=1
        print(list(lists)) # Print each "person" detection

    # names = results.pandas().xyxy[0]['name'].tolist()
    # person_indices = [i for i, name in enumerate(names) if name == 'person']
    # person_results = results.pandas().xyxy[0].iloc[person_indices]
    # print(person_results)
    #print(results.pandas().xyxy[0])