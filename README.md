# DrivePerceptron
## Autonomous Vehicle Camera Perception Kit

![logo_epic](https://github.com/dledesma2000/EEC174B_FinalSample/assets/74477926/d9702984-bc3c-4626-b4d8-478e467666e9)






# Table of Contents

1. [Introduction](#introduction)
2. [Running the Code](#running-the-code)
3. [Main Functionality of the Code](#main-functionality-of-the-code)
    - [yolo_and_line_detection.py](#yolo_and_line_detectionpy)
4. [Line Detection Summary](#line-detection-summary)
    - [Code Modules Summary](#code-modules-summary)
        - [`line_detector.py`](#line_detectorpy)
        - [`color_range.py`](#color_rangepy)
        - [`detections.py`](#detectionspy)
        - [`line_output.py`](#line_outputpy)
5. [Image Processing and Detection Method](#image-processing-and-detection-method)
6. [YOLO Object Detection Module Summary](#yolo-object-detection-module-summary)
    - [`yolo_detection.py`](#yolo_detectionpy)
7. [Visualization Module Summary](#visualization-module-summary)
    - [`plot_detections.py`](#plot_detectionspy)
    - [`print_instruction.py`](#print_instructionpy)
8.  [Scenario Data Analysis Module Summary](#scenario-data-analysis-module-summary)
    - [`box_stat.py`](#`box_stat.py`)
9.  ['Mean Brightness Factor Exploration'](#mean-brightness-factor-exploration)


## Introduction

The Autonomous Vehicle Camera Perception Module integrates YOLO (You Only Look Once) object detection and line detection functionalities to enhance the perception capabilities of autonomous vehicles. This module processes input videos, detects various objects of interest, and generates annotated output videos with instructional text and color maps.

The `yolo_and_line_detection.py` script serves as the core component, combining YOLO object detection and line detection algorithms. Through a series of functions and utilities, it orchestrates the detection of target objects such as stop signs, motorbikes, pedestrians (represented by birds and apples), and cars, while also identifying lane markings and boundaries.

Key functionalities of this module include:
- Utilizing YOLO for robust object detection, including the identification of vehicles, traffic signs, and pedestrians.
- Leveraging line detection algorithms to recognize lane markings and boundaries, crucial for autonomous navigation.
- Annotating output videos with instructional text, providing real-time feedback on detected objects and navigation scenarios.
- Optional analysis for scenarios to explore impact of factors that could affect detection, collects metric data and plots useful graphs.
## Running the Code

To run the code, follow these steps:

1. **Clone the Repository**:
   - Clone the GitHub repository to your local machine by executing the following command in your terminal:

     ```
     git clone https://github.com/dledesma2000/EEC174B_FinalSample.git
     ```

   - This will download the project files to your local directory.

2. **Download YOLO Weights**: 
   - Download the YOLOv3.weights file, which contains the weights for YOLOv3.
   - [Download YOLO weights](https://drive.google.com/uc?export=download&id=1Eg_kl6C9ZHaLc-SkvF77WFoWYwVZVaFX)
   
3. **Place the Downloaded Weights**:
   - Once the weights are downloaded, place the YOLOv3.weights file into your local `yolo_files` folder. This ensures that the code can access the weights during execution.

4. **Run the Code**:
   - Open your terminal or command prompt.
   - Navigate to the directory containing the `yolo_and_line_detection.py` script.
   - Enter the following command into the terminal:

     ```
     python yolo_and_line_detection.py '.\Scenarios\x.mp4'
     ```

     Replace `x` with the name of the scenario you wish to run.
   
   - To run scenarios for analysis and data collection use:
     ```
     python yolo_and_line_detection.py '.\Scenarios\Scenario1.mp4' -analyze
     ```
     
5. **Processing the Video**:
   - Once the command is entered, the video processing will begin.
   
6. **Viewing the Result**:
   - After processing, the resulting annotated video will be saved in the  `.\ScenarioResults\InstructionResults` directory with the corresponding color map in `.\ScenarioResults\ColorMaps`

Following these steps will allow you to successfully run the code and obtain the processed video output.

### Instruction Results Video
This is the visualization for the detections made by YOLO and Line detection

https://github.com/dledesma2000/EEC174B_FinalSample/assets/146287756/bd9ae608-f3f6-4efc-8faa-049e788e4d2b



### Color Map Video
This is the vizualization for the color filter applied on the image to detect lines

https://github.com/dledesma2000/EEC174B_FinalSample/assets/146287756/a0c43a5c-b7ff-4e2b-9f66-f3bf158b1101



## Main Functionality of the code 

### `yolo_and_line_detection.py`

The `yolo_and_line_detection.py` script combines YOLO object detection and line detection functionalities to process input videos and generate output videos with annotations.


#### Functions and Utilities:

1. **`read_cline()`**
   - Parses command-line arguments for input video path.
   - Returns the parsed arguments.

2. **`frameCounter(targetCheck, target_frame_counter)`**
   - Updates the target frame counter based on the presence of a target in the frame.
   - Increases the counter if the target is present, decreases if the target is absent.
   - Returns the updated target frame counter.

3. **`is_value_in_list(my_list, target)`**
   - Checks if a target value exists in a list.
   - Returns `True` if the target value is found, otherwise `False`.

4. **`count_target_value(arr, target)`**
   - Counts the occurrences of a target value in an array.
   - Returns the count of occurrences.

5. **`store_non_repeated(arr)`**
   - Stores non-repeated elements from an array.
   - Returns an array containing only unique elements.

6. **`main()`**
   - Main function to process input video frames.
   - Performs YOLO object detection and line detection on each frame.
   - Generates annotated output videos with instructional text and color maps.
   - Saves the processed videos to output files.

### Important Variables

- **`target_classes`**: An array containing the class IDs of the target objects to be detected using YOLO.
     - 11: Stop Sign
     - 3: Motorbike
     - 14: Bird (Representing Pedestrians because we used a rubber duck)
     - 47: Apple (Representing Pedestrians because we used a rubber duck)
     - 2: Car

- **`class_checks`**: A boolean array indicating whether each target class is present in the current frame.
     - `class_checks[0]`: Stop Sign
     - `class_checks[1]`: Motorbike
     - `class_checks[2]`: Bird 
     - `class_checks[3]`: Apple 
     - `class_checks[4]`: Car

- **`class_counters`**: An array keeping track of the number of consecutive frames in which each target class has been detected.
     - `class_counters[0]`: Stop Sign
     - `class_counters[1]`: Motorbike
     - `class_counters[2]`: Bird
     - `class_counters[3]`: Apple
     - `class_counters[4]`: Car

- **`labelsfiles`**: A list containing the class labels corresponding to the YOLO class IDs. It is populated by reading the class labels from the `coco.names` file.

## Line Detection Summary
The line detection process involves the extraction of line segments from an input image based on specific color ranges. This functionality is achieved through the `LineDetector` class, which integrates edge detection, color filtering, and line segment extraction. The basic framework for this code was provided by Duckietown and can be found [here.](https://github.com/duckietown/dt-core/tree/daffy/packages/line_detector/include/line_detector)

### Code Modules Summary

### `line_detector.py`
The `line_detector.py` module contains the `LineDetector` class, which provides methods for line detection. It includes functions for setting the image, edge detection, line detection using the Hough transform, color filtering, and normal calculation.

### `color_range.py`
The `color_range.py` module defines the `ColorRange` class, which is used for defining color ranges and checking if pixels in an image match any of those ranges. It includes methods for creating color range objects from dictionaries and performing range-based filtering on images.

### `detections.py`
The `detections.py` module contains the `Detections` class, which serves as a data structure for storing the results of line detection. It includes attributes for storing detected lines, normals, region maps, and centers.

### `line_output.py`
The `line_output.py` provides the `line_detections(frame,line_detector)` function which performs line detection on a given frame using a `LineDetector` object.

## Image Processing and Detection Method
The line detection process involves several steps:

1. **Setting the Image**: The `setImage` method in the `LineDetector` class is used to set the input image for processing. This method converts the image to the HSV color space and calls `findEdges`.

2. **Edge Detection**: The `findEdges` method in the `LineDetector` class applies Canny edge detection to the input image and returns the binary edge map.

3. **Line Detection**: The `houghLine` method in the `LineDetector` class performs line detection using the probabilistic Hough transform on the provided binary edge map. It returns an array of line segments.

4. **Color Filtering**: The `colorFilter` method in the `LineDetector` class filters the image to extract regions within the specified color range. It also identifies edges in these regions and applies dilation for smoothing.

5. **Normal Calculation**: The `findNormal` method in the `LineDetector` class calculates the centers and normals of detected line segments.

6. **Detection Method**: The `detectLines` method in the `LineDetector` class combines the color filtering and line detection methods to detect line segments within the specified color range. It returns a `Detections` object containing the detected lines, normals, region maps, and centers.

## YOLO Object Detection Module Summary

### `yolo_detection.py`

This module provides functionalities for detecting objects using the YOLO (You Only Look Once) algorithm.
#### Functions:

1. **load_yolo(weights, config)**
   - Loads the YOLO network model from the given weights and configuration files.
   - Returns the loaded network and the names of the YOLO layers.

2. **BBCC(output, image, probability_minimum, threshold, h, w, target_class)**
   - Generates bounding boxes for detected objects based on the YOLO output.
   - Filters out bounding boxes based on probability and target classes.
   - Returns the bounding boxes, confidences, and classes of detected objects.

3. **BoxDrawing(frame, results, bounding_boxes, class_names, classes)**
   - Draws bounding boxes around detected objects on the input frame.
   - Displays the class names of detected objects.
   - Returns the frame with bounding boxes and class labels drawn.

4. **run_yolo(frame, network, yolo_layers, probability_minimum, threshold, target_classes)**
   - Performs YOLO object detection on the input frame using the provided YOLO network.
   - Filters out detected objects based on probability and target classes.
   - Returns the bounding boxes, confidences, classes, and results of detected objects.

## Visualization Module Summary

### `plot_detections.py`
The `plot_detections.py` module provides functions for visualizing line segment detections and color filter maps on images.
### Functions
1. **`plotSegments(image, detections):`** Draws detected line segments and their normals on an input image.

2. **`plotMaps(image, detections):`** Draws color filter maps on an input image.

### `print_instruction.py`

The `print_instruction.py` module provides functions for printing instructional text on images.

#### Functions:

1. **`get_display_action(class_checks, class_counters, class_lost)`**
   - Determines the action message to display based on class checks, counters, and class lost status.
   - "Stopped" message gets printed when `class_checks[0]` is `True` and `class_counters[0]` is between 30 and 90.
   - "Stopping" message gets printed when `class_lost` is less than 30 or `class_checks[0]` or `class_checks[4]` are `True`, and `class_counters[0]` is greater than 89.
   - Returns the action message to display.

2. **`get_display_scenario(class_checks, class_counter, segments)`**
   - Determines the scenario message to display based on class checks, class counter, and segment detection status.
   - "2 Way Intersection" message gets printed when `class_counter[0]` is greater than 1 and `segments` is `True`.
   - Returns the scenario message to display.

3. **`put_time_on_frame(frame, current_frame, frame_rate)`**
   - Displays the current time of the video on the input frame.
   - Calculates the current time in minutes and seconds based on the current frame number and frame rate.
   - Prints the time at the top-right corner of the frame.
   - Returns the frame with the time displayed.

4. **`print_text_center_top(frame, text)`**
   - Prints text at the center-top position of the input frame.
   - Calculates the position to print the text at the center-top of the frame.
   - Prints the text on the frame.
   - Returns the frame with the text printed at the center-top position.

5. **`print_text_bottom_left(frame, text)`**
   - Prints text at the bottom-left position of the input frame.
   - Calculates the position to print the text at the bottom-left of the frame.
   - Prints the text on the frame with reduced font scale.
   - Returns the frame with the text printed at the bottom-left position.

6. **`print_text_bottom_right(frame, classes, labelsfiles)`**
   - Prints text at the bottom-right position of the input frame.
   - Iterates over the detected classes and appends the corresponding labels.
   - Calculates the position to print the text at the bottom-right of the frame.
   - Prints each line of text on the frame.
   - Returns the frame with the text printed at the bottom-right position.
  

## Scenario Data Analysis Module Summary

### `box_stat.py`
The `box_stat.py` script uses matplotlib and numpy to measure bounding box mean brightness for the test scenarios, as well as other metrics such as average inference time to present data as part of the scenario factor breakdown pipeline.

### Functions
1. **` mean_brightness(frame, bounding_box):`** Computes average brightness of bounding box using Gray-Scale conversion to measure pixel intensity. 

2. **`BoundingBoxClassify(frame, bounding_boxes, classes, confidences):`** Compute average brightness for different classes seperately.

3. **`StatstoFile(total_stats, output_file,inference_times,input_video_filename,car_counter, stop_sign_counter, frame_number, car_ratio_top, stop_sign_ratio_top):`** Write statistics of road object-confidence-mean_brightness to a file and other metrics.
4. **`SummarytoFile(output_file,inference_times,input_video_filename,car_counter, stop_sign_counter, frame_number, car_ratio_top, stop_sign_ratio_top):`** Write summary of metrics and measurements to a file.
5. **`Mean_Brightness_Road_Objects(total_stats,save_path):`** Plot mean brightness for different road objects.
6. **`Mean_Brightness_Stop_Sign_Confidence(total_stats,save_path):`** Plot mean brightness for stop signs and their confidence.
7. **`Mean_Brightness_Car_Confidence(total_stats,save_path):`** Plot mean brightness for cars and their confidence.

### Mean Brightness Factor Exploration 
The selected factor for exploration was the mean brightness because image brightness of a specific Region of Interest (RoI) can affect its color intensity, luminosity, contrast with the environment as well as texture. This is measured via gray-scale conversion to measure pixel intensity. 

Here are examples of some plots using this exploration pipeline:

## Different Road Objects Mean Brightness Plot:
![{input_video_filename}-road_object_brightness](https://github.com/dledesma2000/EEC174B_FinalSample/assets/74477926/6cbd98a9-7b6c-4fcd-8044-735669dc8174)

## Mean Brightness vs Confidence for Cars :

![{input_video_filename}-car_confidence_brightness_graph](https://github.com/dledesma2000/EEC174B_FinalSample/assets/74477926/69512f8e-9499-4448-a851-01b2fda9fee0)


## Mean Brightness vs Confidence for Stop Sign:


![{input_video_filename}-stop_sign_confidence_brightness_graph](https://github.com/dledesma2000/EEC174B_FinalSample/assets/74477926/56416f02-bc9a-4161-8e03-e52e989aeaa1)


To view the full exploration, motivation and analysis please follow the results from the report. 

