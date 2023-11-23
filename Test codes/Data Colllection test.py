import cv2
import dlib
import json

# Load the pre-trained face detector and shape predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Create a VideoCapture object
cap = cv2.VideoCapture(0)

# Set the window to full screen
cv2.namedWindow("Gaze Tracking", cv2.WINDOW_FULLSCREEN)
cv2.setWindowProperty("Gaze Tracking", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Get the screen width and height
screen_width = int(cap.get(3))
screen_height = int(cap.get(4))

# JSON file path
json_file_path = "iris_data.json"

# Load existing data from the JSON file
try:
    with open(json_file_path, "r") as json_file:
        json_data = json.load(json_file)
except FileNotFoundError:
    # If the file doesn't exist, initialize an empty dictionary
    json_data = {"circles": [], "left_irises": [], "right_irises": []}

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Store the position of the clicked circle
        json_data["circles"].append({"x": x, "y": y})

        # Detect face and landmarks
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        if len(faces) > 0:
            landmarks = predictor(gray, faces[0])

            # Store the positions of left and right irises
            left_eye = landmarks.part(42).x, landmarks.part(42).y
            right_eye = landmarks.part(45).x, landmarks.part(45).y
            json_data["left_irises"].append({"x": left_eye[0], "y": left_eye[1]})
            json_data["right_irises"].append({"x": right_eye[0], "y": right_eye[1]})

# Create a fullscreen window with five circles at corners and center
cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

cv2.setMouseCallback("Video", mouse_callback)

while True:
    ret, frame = cap.read()

    # Draw five circles
    circle_radius = 10
    circle_color = (0, 255, 0)  # Green color

    # Shift the top-center circle to the middle of the screen
    circle_radius = 10
    circle_color = (255, 0, 0)  # Blue color

    # Calculate circle positions
    top_center_circle_position = (screen_width // 2, screen_height // 4 )
    top_left_circle_position = (circle_radius * 2, circle_radius * 2)
    top_right_circle_position = (screen_width - circle_radius * 2, circle_radius * 2)
    middle_left_circle_position = (circle_radius * 2, screen_height // 2)
    middle_center_circle_position = (screen_width // 2, screen_height // 2)
    middle_right_circle_position = (screen_width - circle_radius * 2, screen_height // 2)
    bottom_left_circle_position = (circle_radius * 2, screen_height - circle_radius * 2)
    bottom_center_circle_position = (screen_width // 2, screen_height - circle_radius * 2)
    bottom_right_circle_position = (screen_width - circle_radius * 2, screen_height - circle_radius * 2)

    # Draw circles on the frame
    cv2.circle(frame, top_center_circle_position, circle_radius, circle_color, -1)  # Middle-center
    cv2.circle(frame, top_left_circle_position, circle_radius, circle_color, -1)  # Top-left
    cv2.circle(frame, top_right_circle_position, circle_radius, circle_color, -1)  # Top-right
    cv2.circle(frame, middle_left_circle_position, circle_radius, circle_color, -1)  # Middle-left
    cv2.circle(frame, middle_center_circle_position, circle_radius, circle_color, -1)  # Middle-center
    cv2.circle(frame, middle_right_circle_position, circle_radius, circle_color, -1)  # Middle-right
    cv2.circle(frame, bottom_left_circle_position, circle_radius, circle_color, -1)  # Bottom-left
    cv2.circle(frame, bottom_center_circle_position, circle_radius, circle_color, -1)  # Bottom-center
    cv2.circle(frame, bottom_right_circle_position, circle_radius, circle_color, -1)  # Bottom-right
    
    # Display the frame
    cv2.imshow("Video", frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Save the updated data to the JSON file
with open(json_file_path, "w") as json_file:
    json.dump(json_data, json_file, indent=2)

# Release the VideoCapture and close the OpenCV window
cap.release()
cv2.destroyAllWindows()