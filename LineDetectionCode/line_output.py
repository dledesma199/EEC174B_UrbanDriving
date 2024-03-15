from .line_detector import LineDetector
from .color_range import ColorRange
from .detections import Detections




def line_detections(frame,line_detector):
    line_detector.setImage(frame)
    # yellow_range = ColorRange.fromDict({'low': [5, 100, 100], 'high': [35, 255, 255]})
    # yellow_range = ColorRange.fromDict({'low': [15, 100, 100], 'high': [45, 255, 255]})
    yellow_range = ColorRange.fromDict({'low': [10, 75, 100], 'high': [70, 255, 255]})
    white_range = ColorRange.fromDict({'low': [0, 0, 150], 'high': [180, 50, 255]})
    red_range = ColorRange.fromDict({'low': [170, 100, 100], 'high': [10, 255, 255]})
    # Detect lines using the LineDetector for each color range
    yellow_detections = line_detector.detectLines(yellow_range)
    white_detections = line_detector.detectLines(white_range)
    red_detections = line_detector.detectLines(red_range) 
    # Merge detections 
    if (yellow_detections):
        yellow_check = True
    else:
        yellow_check = False
    
    if (white_detections):
        white_check = True
    else:
        white_check = False
    
    white_check = True
    combined_detections = {yellow_range: yellow_detections, white_range: white_detections, red_range : red_detections}

    return combined_detections, yellow_check, white_check 

    