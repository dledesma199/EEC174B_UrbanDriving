import numpy as np
# import pandas as pd
import cv2
import argparse
# import os
from LineDetectionCode.line_detector import LineDetector
from LineDetectionCode.line_output import line_detections
from YoloCode.yolo_detection import load_yolo, BoxDrawing, run_yolo
from YoloCode.box_stat import BoundingBoxClassify, StatstoFile, Mean_Brightness_Stop_Sign_Confidence, Mean_Brightness_Road_Objects, Mean_Brightness_Car_Confidence, SummarytoFile, frame_det_ratio
from VisualizationCode.print_instruction import *
from VisualizationCode.plot_detections import plotSegments, plotMaps






def read_cline():
    parser = argparse.ArgumentParser(description='Duckietown Lane Detector')
    parser.add_argument('input_video', type=str, help='Path to the input video file')
    parser.add_argument('-analyze', action='store_true', help='Option to collect detection metrics and store them in a file')
    return parser.parse_args()

def frameCounter(targetCheck, target_frame_counter):
    if targetCheck:
        target_frame_counter += 1
    elif not targetCheck and target_frame_counter > 0:
        target_frame_counter -= 1
    return target_frame_counter

def is_value_in_list(my_list, target):
    for value in my_list:
        if value == target:
            return True
    return False

def count_target_value(arr, target):
    count = 0
    for value in arr:
        if value == target:
            count += 1
    return count

def store_non_repeated(arr):
    unique_values = []
    for element in arr:
        if element not in unique_values:
            unique_values.append(element)
    return unique_values

def main():
    
    stop_sign_lost = 0
    probability_minimum = 0.5
    threshold = 0.15
    target_classes = [11,3,14,47,2]

    class_checks = [False] * len(target_classes)
    class_counters = [0 for _ in target_classes]
    car_counter = 0
    stop_sign_counter = 0

    stop_sign_ratio_top = 0
    car_ratio_top = 0

    class_detections = [] 
    labelsfiles = []
    labelsfiles = open('yolo_files/coco.names').read().strip().split('\n')

    frame_rate = 30
    current_frame_number = 0

    args = read_cline()

    line_detector = LineDetector()
    
    # Open the input video file
    input_video_path = args.input_video
    cap = cv2.VideoCapture(input_video_path)
    network, yolo_layers = load_yolo('yolo_files/yolov3.weights', 'yolo_files/yolov3.cfg')
    ret, frame = cap.read()
    h, w = frame.shape[:2]
    # Define the output video path with dynamic filename
    input_video_filename = args.input_video.split('\\')[-1].split('.')[0]
    OutVideo = cv2.VideoWriter(f"./ScenarioResults/InstructionResults/{input_video_filename}-result.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 30, (w, h))
   
    ColorMapVideo = cv2.VideoWriter(f"./ScenarioResults/ColorMaps/{input_video_filename}-ColorMap.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 30, (w, h))
    #static video path
    # OutVideo = cv2.VideoWriter("./ScenarioResults/InstructionResults/Scenario2-result.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 30, (w, h))
    ColorMapVideo = cv2.VideoWriter("./ScenarioResults/ColorMaps/Scenario2-ColorMap.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 30, (w, h))
    inference_times = []
    total_stats = []
    # Your video processing loop
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        current_frame_number += 1
        yolo_frame = frame.copy()
        line_frame = frame.copy() 
        segment_detections = line_detections(line_frame,line_detector)
        bounding_boxes, confidences, classes, results, inference_time = run_yolo(yolo_frame,network,yolo_layers,probability_minimum,threshold,target_classes)
     

        

            
        

        

        
        class_detections = store_non_repeated(classes)
        for i, target_class in enumerate(target_classes):
            class_checks[i] = is_value_in_list(classes, target_class)
        for i in range(len(target_classes)):
            class_counters[i] = frameCounter(class_checks[i], class_counters[i])
        
        
        if(class_checks[0] == False):
            stop_sign_lost += 1 
        else:
            stop_sign_lost = 0
        
        frame = plotSegments(frame, segment_detections)
        frame1 = plotMaps(frame,segment_detections)
        frame = BoxDrawing(frame,results,bounding_boxes,labelsfiles,classes)
        action_to_display = get_display_action(class_checks, class_counters,stop_sign_lost)
        scenario_to_display = get_display_scenario(class_checks,stop_sign_counter,segment_detections)
        frame = print_text_center_top(frame, action_to_display)
        frame - print_text_bottom_left(frame,scenario_to_display)
        frame = print_text_bottom_right(frame, class_detections,labelsfiles)
        frame = put_time_on_frame(frame,current_frame_number,frame_rate)
        inference_times.append(inference_time)
        if args.analyze:
            
            stats = BoundingBoxClassify(frame, bounding_boxes, classes, confidences)
            stop_sign_present = False
            car_present = False
            for s in stats:
                if s[1] == 2:
                    car_counter += 1
                    car_present = True
                elif s[1] == 11:
                    stop_sign_counter += 1
                    stop_sign_present = True
            if car_present == True:
                car_ratio_top += 1
            if stop_sign_present == True:
                stop_sign_ratio_top += 1

            
            total_stats.append(stats)
       
        OutVideo.write(frame)                                 
        ColorMapVideo.write(frame1)
        #cv2.imshow('frame',frame)
        #cv2.imshow('Color Map',frame1) 
        if cv2.waitKey(1) == ord('q'):
            break
    if(args.analyze):
        #StatstoFile(total_stats, output_file,inference_times,input_video_filename, car_counter, stop_sign_counter,current_frame_number,car_ratio_top,stop_sign_ratio_top)

        output_file = f"./ScenarioResults/Stats/{input_video_filename}-stats-raw.txt"
        output_summary = f"./ScenarioResults/Stats/{input_video_filename}-stats-summary.txt"

        SummarytoFile(output_summary,inference_times,input_video_filename,car_counter, stop_sign_counter, current_frame_number, car_ratio_top, stop_sign_ratio_top)
        Mean_Brightness_Stop_Sign_Confidence(total_stats,f"./ScenarioResults/Plots/{input_video_filename}-stop_sign_confidence_brightness_graph.png")
        Mean_Brightness_Road_Objects(total_stats,f"./ScenarioResults/Plots/{input_video_filename}-road_object_brightness.png")
        Mean_Brightness_Car_Confidence(total_stats,f"./ScenarioResults/Plots/{input_video_filename}-car_confidence_brightness_graph.png")
    avg_inference_time = np.mean(inference_times)
    print("Average inference time: ", avg_inference_time)
    # Release resources
    cap.release()
    OutVideo.release()
    ColorMapVideo.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()