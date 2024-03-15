import cv2
import numpy as np
import time

def load_yolo(weights, config):
    network = cv2.dnn.readNetFromDarknet(config, weights) #take generic config and weights
    yolo_layers = ['yolo_82', 'yolo_94', 'yolo_106']
    return network, yolo_layers

def BBCC(output, image, probability_minimum, threshold, h, w,target_class):     #generate bounding boxes
    bounding_boxes = []
    confidences = []
    classes = []
    for result in output:
        for detection in result:
            scores = detection[5:]
            class_current = np.argmax(scores)
            confidence_current = scores[class_current]
            #and class_current == target_class
            if confidence_current > probability_minimum and class_current in target_class:      #only make boxes for the target classes
                box_current = detection[0:4] * np.array([w, h, w, h])
                x_center, y_center, box_width, box_height = box_current.astype('int')
                x_min = int(x_center - (box_width / 2))
                y_min = int(y_center - (box_height / 2))
                bounding_boxes.append([x_min, y_min, int(box_width), int(box_height)])
                confidences.append(float(confidence_current))
                classes.append(class_current)
    return bounding_boxes, confidences, classes




def BoxDrawing(frame, results, bounding_boxes,class_names,classes):
    if len(results) > 0:
        for i in results.flatten():
            class_id = classes[i]
            class_name = class_names[class_id]
            x_min, y_min = bounding_boxes[i][0], bounding_boxes[i][1]
            box_width, box_height = bounding_boxes[i][2], bounding_boxes[i][3]
            colour_box = (255, 0, 0)  # Blue color
            cv2.rectangle(frame, (x_min, y_min), (x_min + box_width, y_min + box_height), colour_box, 5)
            colour_text = (0, 0, 0)  # Black color
            # Set label to be the class name of the detection
            label = f"{class_name}"
            # Calculate the font scale dynamically based on the width of the bounding box
            font_scale = min(box_width, box_height) / (len(label) * 0.6)
            # Adjust the font scale if it's too large
            font_scale = min(font_scale, 1.0)
            # Calculate text size to get the text width and height
            (text_width, text_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)
            # Calculate text position so it's centered horizontally and at the top of the bounding box
            text_x = x_min + (box_width - text_width) // 2
            text_y = y_min - 7  # Adjust this value to position the text where you want
            # Draw the text
            cv2.putText(frame, label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, colour_text, 2)
    return frame

def run_yolo(frame,network,yolo_layers,probability_minimum,threshold,target_classes):
    input_blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    start_time = time.time()
    network.setInput(input_blob)
    output = network.forward(yolo_layers)
    # Calculate inference time
    inference_time = time.time() - start_time

    h, w = frame.shape[:2]                                                                              #define boundaries for the bounding boxes
    bounding_boxes, confidences, classes = BBCC(output, frame, probability_minimum, threshold, h, w,target_classes)
    results = cv2.dnn.NMSBoxes(bounding_boxes, confidences, probability_minimum, threshold)             #this function returns a list of indices corresponding to the kept bounding boxes


    # Add inference time
    return  bounding_boxes, confidences, classes, results, inference_time