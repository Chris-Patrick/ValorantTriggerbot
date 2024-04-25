import cv2
import numpy as np
import pyautogui
import mss
import time
import keyboard
import random
from pynput.mouse import Button, Controller

# Set target color in BGR format
purple = (0, 0, 255)
red  = (152, 20, 37)


# Set crosshair coordinates
crosshair_x = 957
crosshair_y = 536

# Set region of interest (ROI) dimensions
roi_width = 5
roi_height = 5

# Set delay between trigger actions (in seconds)
action_delay = round(random.uniform(0.001, 0.005), 3)

# Disable PyAutoGUI fail-safe
pyautogui.FAILSAFE = False

# Create a named window for the debug display
cv2.namedWindow("Debug Window", cv2.WINDOW_NORMAL)

# Flag to determine if the script should run or not
running = False

def toggle_script(event):
    global running

    if event.event_type == "down":
        running = True
    elif event.event_type == "up":
        running = False

keyboard.on_press_key("left shift", toggle_script)
keyboard.on_release_key("left shift", toggle_script)

# Convert target color to LAB color space
with mss.mss() as sct:
    # Set monitor coordinates to capture the crosshair area
    monitor = {"top": crosshair_y, "left": crosshair_x, "width": roi_width, "height": roi_height}

    while True:
        # Check if the script should run
        if running:
            # Capture screen frame
            frame = np.array(sct.grab(monitor))

            # Convert frame to BGR format
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)

            # Convert frame to HSV color space
            frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Define lower and upper bounds for the target color in HSV
            lower_bound = np.array([140, 70, 70])
            upper_bound = np.array([160, 255, 255])

            # Create a mask to filter pixels within the target color range
            mask = cv2.inRange(frame_hsv, lower_bound, upper_bound)

            # Check if any pixels match the color
            if np.any(mask):
                # Perform trigger action
                pyautogui.mouseDown(button='left')
                print("Worked")
                #time.sleep(.005)
                pyautogui.mouseUp(button='left')
                print("Worked")

                # Delay between actions
                time.sleep(action_delay)

            # Display the frame in the debug window
            cv2.imshow("Debug Window", frame)

        # Exit loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord("l"):
            break

cv2.destroyAllWindows()