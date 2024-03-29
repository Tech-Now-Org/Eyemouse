import cv2
import pyautogui

# Get screen resolution
screen_width, screen_height = pyautogui.size()

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Function to map eye movements to mouse cursor within screen bounds
def control_mouse(x, y):
    # Map eye coordinates to screen coordinates within bounds
    target_x = int(x * screen_width)
    target_y = int(y * screen_height)
    # Limit cursor movement within screen bounds
    target_x = max(0, min(target_x, screen_width - 1))
    target_y = max(0, min(target_y, screen_height - 1))
    # Move the mouse cursor
    pyautogui.moveTo(target_x, target_y)

# Initialize variables for blink detection
prev_left_eye_state = False
prev_right_eye_state = False

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert frame to grayscale for eye detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect eyes in the grayscale frame
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
    
    # Reset blink counters
    left_eye_state = False
    right_eye_state = False
    
    for (ex, ey, ew, eh) in eyes:
        # Calculate the center of the eye region
        eye_center_x = ex + ew // 2
        eye_center_y = ey + eh // 2
        # Normalize eye coordinates (0 to 1)
        norm_eye_x = eye_center_x / frame.shape[1]
        norm_eye_y = eye_center_y / frame.shape[0]
        # Control the mouse cursor based on eye center
        control_mouse(norm_eye_x, norm_eye_y)
        
        # Determine if the eye is open or closed based on aspect ratio of the eye region
        aspect_ratio = ew / eh
        if aspect_ratio < 0.2:  # Adjust this threshold based on your setup
            left_eye_state = True if eye_center_x < frame.shape[1] // 2 else False
            right_eye_state = True if eye_center_x > frame.shape[1] // 2 else False
    
    # Perform click actions based on blink detection
    if prev_left_eye_state and not left_eye_state:
        # Left eye blinked
        pyautogui.click(button='left')
    elif prev_right_eye_state and not right_eye_state:
        # Right eye blinked
        pyautogui.click(button='right')
    
    # Update previous eye states
    prev_left_eye_state = left_eye_state
    prev_right_eye_state = right_eye_state
    
    # Display the video feed
    cv2.imshow('Eye Tracking', frame)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
