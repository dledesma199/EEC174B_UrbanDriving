import cv2
import numpy as np
import matplotlib.pyplot as plt



def mean_brightness(frame, bounding_box):
    # Calculate mean brightness of a bounding box
    x, y, w, h = bounding_box
    roi = frame[y:y+h, x:x+w]
    mean_brightness = np.mean(cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY))
    return mean_brightness




def BoundingBoxClassify(frame, bounding_boxes, classes, confidences):
        # Classify bounding boxes
        f = []
        cls = ""
        for box, confidence, class_id in zip(bounding_boxes, confidences, classes):
            mean_brightness_box = mean_brightness(frame, box)
            if class_id == 2:
                cls = "Car"
            elif class_id == 11:
                cls = "Stop sign"
            f.append([mean_brightness_box, cls, confidence])
            
        return f


    
        
   
def StatstoFile(total_stats, output_file,inference_times,input_video_filename,car_counter, stop_sign_counter, frame_number, car_ratio_top, stop_sign_ratio_top):
    # Write statistics to a file
    avg_inference_time = np.mean(inference_times)
    with open(output_file, 'w') as f:
        f.write("Video file: {}\n".format(input_video_filename))
        f.write("Total frames: {}\n".format(frame_number))
        f.write("Average inference time: {}\n".format(avg_inference_time))
        f.write("Car counter: {}\n".format(car_counter))
        f.write("Stop sign counter: {}\n".format(stop_sign_counter))
        f.write("Car detection rate: {}\n".format(car_ratio_top/frame_number))
        f.write("Stop sign detection rate: {}\n".format(stop_sign_ratio_top/frame_number))
        f.write("\n")
        for i in range(len(total_stats)):
            f.write("Frame number: {}\n".format(i+1))
            f.write("\n")
            for obj in total_stats[i]:
                f.write("   Class ID: {}\n".format(obj[1]))
                f.write("   Mean brightness: {}\n".format(obj[0]))
                f.write("   Confidence: {}\n".format(obj[2]))
                f.write("\n")
    f.close()

def SummarytoFile(output_file,inference_times,input_video_filename,car_counter, stop_sign_counter, frame_number, car_ratio_top, stop_sign_ratio_top):
    # Write summary statistics to a file
    avg_inference_time = np.mean(inference_times)
    with open(output_file, 'w') as f:
        f.write("Video file: {}\n".format(input_video_filename))
        f.write("Total frames: {}\n".format(frame_number))
        f.write("Average inference time: {}\n".format(avg_inference_time))
        f.write("Car counter: {}\n".format(car_counter))
        f.write("Stop sign counter: {}\n".format(stop_sign_counter))
        f.write("Car detection rate: {}\n".format(car_ratio_top/frame_number))
        f.write("Stop sign detection rate: {}\n".format(stop_sign_ratio_top/frame_number))
        f.write("\n")
    f.close()


def Mean_Brightness_Road_Objects(total_stats,save_path):
    
    # Plot mean brightness for different road objects
    mean_brightness_arr = []
    b_car = []
    b_stop = []
    cls_s = ["Car", "Stop sign"]
    for i in range(len(total_stats)):
        for obj in total_stats[i]:
            cls = obj[1]
            if(cls == "Car"):
                b_car.append(obj[0])
            else:
                b_stop.append(obj[0])
            mean_brightness_arr.append(obj[0])
            
    av_car = np.mean(b_car)
    av_stop = np.mean(b_stop)

    
    colors = ['#1f77b4' if cls == "Car" else '#ff7f0e' for cls in cls_s]

    plt.bar(cls_s, [av_car, av_stop], color=colors)
    plt.xlabel('Road Objects')
    plt.ylabel('Average Mean Brightness')
    plt.title('Average Mean Brightness for Different Road Objects')
    for i, v in enumerate([av_car, av_stop]):
        plt.text(i, v, f'{v:.2f}', ha='center', va='bottom')
    plt.xticks(cls_s)
    plt.savefig(save_path)
    plt.close()

def Mean_Brightness_Stop_Sign_Confidence(total_stats,save_path):
    # Plot mean brightness for stop signs and their confidence
    mean_brightness_arr = []
    conf_arr = []
    for i in range(len(total_stats)):
        for obj in total_stats[i]:
            cls = obj[1]
            if(cls == "Stop sign"):
                mean_brightness_arr.append(obj[0])
                conf_arr.append(obj[2])
    plt.scatter(mean_brightness_arr, conf_arr)
    plt.xlabel('Mean Brightness')
    plt.ylabel('Confidence')
    plt.title('Mean Brightness vs Confidence for Stop Signs')
    plt.savefig(save_path)
    plt.close()

def Mean_Brightness_Car_Confidence(total_stats,save_path):
    # Plot mean brightness for cars and their confidence
    mean_brightness_arr = []
    conf_arr = []
    for i in range(len(total_stats)):
        for obj in total_stats[i]:
            cls = obj[1]
            if(cls == "Car"):
                mean_brightness_arr.append(obj[0])
                conf_arr.append(obj[2])
    plt.scatter(mean_brightness_arr, conf_arr)
    plt.xlabel('Mean Brightness')
    plt.ylabel('Confidence')
    plt.title('Mean Brightness vs Confidence for Cars')
    plt.savefig(save_path)
    plt.close()


def frame_det_ratio(start_frame, end_frame, total_stats, target_class):
    # Calculate the detection ratio for a target class
    det = 0
    for i in range(start_frame, end_frame):
        for obj in total_stats[i]:
            if obj[1] == target_class:
                det += 1
    return det/(end_frame - start_frame)

    
            