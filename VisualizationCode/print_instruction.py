import cv2

# def get_display_action(class_checks, class_counters, class_lost):
#     # Messages and their priority
#     messages = {
#         "Stopped": (False, 0),
#         "Stopping": (False, 1),
#         "Proceeding Route": (False, 2)
#     }

#     # Check each condition
#     if class_checks[0] and class_checks[4] and (30 <= class_counters[0] <= 90):
#         messages["Stopping"] = (True, messages["Stopping"][1])
#     if class_checks[0] and not class_checks[4] and class_counters[0] > 600:
#         messages["Proceeding Route"] = (True, messages["Proceeding Route"][1])
#     if class_checks[0] or class_checks[4] and class_counters[0] > 90:
#         messages["Stopped"] = (True, messages["Stopped"][1])

#     # Decide which message to display based on priority
#     text_to_display = "Proceeding Route"  # Default message
#     highest_priority = -1
#     for message, (condition_met, priority) in messages.items():
#         if condition_met and priority > highest_priority:
#             highest_priority = priority
#             text_to_display = message

#     return text_to_display

# def get_display_action(class_checks, class_counters, class_lost):
#     # Messages and their priority
#     messages = {
#         "Stopped": (False, 0),
#         "Stopping": (False, 1),
#         "Proceeding Route": (False, 2)
#     }

#     # Check each condition
#     if class_checks[4]:
#         messages["Stopped"] = (True, messages["Stopped"][1])
#     if class_checks[0] and class_checks[4] and (0 <= class_counters[0] <= 90):
#         messages["Stopping"] = (True, messages["Stopping"][1])
#     if class_checks[0] and not class_checks[4] and (class_counters[0] > 270 or class_lost > 60):
#         messages["Proceeding Route"] = (True, messages["Proceeding Route"][1])
#     elif class_checks[0] and class_counters[0] > 90:
#         messages["Stopped"] = (True, messages["Stopped"][1])

#     # Decide which message to display based on priority
#     text_to_display = "Proceeding Route"  # Default message
#     highest_priority = -1
#     for message, (condition_met, priority) in messages.items():
#         if condition_met and priority > highest_priority:
#             highest_priority = priority
#             text_to_display = message

#     return text_to_display
def get_display_action(class_checks, class_counters, class_lost):
    # Messages and their priority
    messages = {
        "Stopped": (False, 0),
        "Stopping": (False, 1),
        "Proceeding Route": (False, 2)
    }

    # Check each condition
    if class_checks[4]:
        # If the car is detected, display the "Stopped" message
        messages["Stopped"] = (True, messages["Stopped"][1])
    elif class_checks[0] and class_checks[4] and (0 <= class_counters[0] <= 90):
        messages["Stopping"] = (True, messages["Stopping"][1])
    elif class_checks[0] and not class_checks[4] and (class_counters[0] > 270 or class_lost > 60):
        messages["Proceeding Route"] = (True, messages["Proceeding Route"][1])
    elif class_checks[0] or class_checks[2] or class_checks[3]:  # Check for apple or bird
        messages["Stopped"] = (True, messages["Stopped"][1])

    # Decide which message to display based on priority
    text_to_display = "Proceeding Route"  # Default message
    highest_priority = -1
    for message, (condition_met, priority) in messages.items():
        if condition_met and priority > highest_priority:
            highest_priority = priority
            text_to_display = message

    return text_to_display



def get_display_scenario(class_checks, class_counter,segments,segment_checks):
    # Messages and their priority
    
    messages = {
        "Lane": (False, 0),
        "2 Way Intersection": (False, 1),  
    }

    # Check each condition
    if(segment_checks[0] and segment_checks[1]):
        messages["Lane"] = (True, messages["Lane"][1])
    if (class_counter > 1) or (segments and class_checks[0]):
        messages["2 Way Intersection"] = (True, messages["2 Way Intersection"][1])
    

    # Decide which message to display based on priority
    text_to_display = "Undetermined"  # Default message
    highest_priority = -1
    for message, (condition_met, priority) in messages.items():
        if condition_met and priority > highest_priority:
            highest_priority = priority
            text_to_display = message

    return text_to_display + " detected"


def put_time_on_frame(frame, current_frame, frame_rate):
    # Calculate current time in the video in seconds
    current_time_seconds = current_frame / frame_rate
    
    # Convert it to minutes and seconds for readability
    minutes = int(current_time_seconds // 60)
    seconds = int(current_time_seconds % 60)
    time_str = f"{minutes:02d}:{seconds:02d}"
    
    # Position of the text: top right corner
    # Adjust the positioning based on your video resolution and desired placement
    text_position = (frame.shape[1] - 150, 30)  # frame.shape[1] is the width of the frame
    
    # Draw the text on the frame
    cv2.putText(frame, time_str, text_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    return frame

def print_text_center_top(frame, text):
    # Get the dimensions of the frame
    frame_height, frame_width, _ = frame.shape

    # Get the size of the text
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]

    # Calculate the position to print the text
    text_x = (frame_width - text_size[0]) // 2
    text_y = text_size[1] + 10  # 10 pixels below the top edge

    # Print the text on the frame
    cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    return frame

def print_text_bottom_left(frame, text):
    # Get the dimensions of the frame
    frame_height, frame_width, _ = frame.shape

    # Get the size of the text
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]

    # Calculate the position to print the text
    text_x = 10  # 10 pixels from the left edge
    text_y = frame_height - 10  # 10 pixels from the bottom edge

    # Reduce the font scale to half
    font_scale = 0.5

    # Print the text on the frame with the adjusted font scale
    cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 255), 2)

    return frame

def print_text_bottom_right(frame, classes, labelsfiles):
    # Get the dimensions of the frame
    frame_height, frame_width, _ = frame.shape

    # Initialize an empty string to store the text
    text_to_display = ""

    # Iterate over the classes array
    for class_idx in classes:
        # Get the class label from the labelsfiles array
        class_label = labelsfiles[class_idx]

        # Append " detected" to the class label and add a newline character
        text_to_display += f"{class_label} detected\n"

    # Remove the trailing newline character
    text_to_display = text_to_display.strip()

    # Get the size of the text
    text_size = cv2.getTextSize(text_to_display, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]

    # Calculate the position to print the text
    text_x = frame_width - text_size[0] - 10  # 10 pixels from the right edge
    text_y = frame_height - 10  # 10 pixels from the bottom edge

    # Split the text into lines
    lines = text_to_display.split('\n')

    # Calculate the total height of all lines of text
    total_text_height = text_size[1] * len(lines)

    # Adjust the starting y-coordinate to align with the bottom of the frame
    text_y -= total_text_height

    # Print each line of text on the frame
    for line in lines:
        # Get the size of the current line of text
        line_size = cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]

        # Calculate the x-coordinate for the current line of text
        line_x = frame_width - line_size[0] - 10  # 10 pixels from the right edge

        # Print the text on the frame
        cv2.putText(frame, line, (line_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Move to the next line
        text_y += line_size[1]

    return frame




