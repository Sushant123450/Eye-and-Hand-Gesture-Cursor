import numpy as np
import cv2
import dlib
import json
import pyautogui

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
            # left_eye = landmarks.part(42).x, landmarks.part(42).y
            # right_eye = landmarks.part(45).x, landmarks.part(45).y
            left_eye = landmarks.part(36).x, landmarks.part(36).y
            right_eye = landmarks.part(45).x, landmarks.part(45).y
            json_data["left_irises"].append(
                {
                    "x": left_eye[0] / float(width) * screen_width,
                    "y": left_eye[1] / float(height) * screen_height,
                }
            )
            json_data["right_irises"].append(
                {
                    "x": right_eye[0] / float(width) * screen_width,
                    "y": right_eye[1] / float(width) * screen_height,
                }
            )

screen_width, screen_height = pyautogui.size()

print(f"Screen Dimensions: {screen_width} x {screen_height}")

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("Test codes\shape_predictor_68_face_landmarks.dat")

# Create a VideoCapture object
cap = cv2.VideoCapture(1)

# Get the screen width and height
screen_width = int(cap.get(3))
screen_height = int(cap.get(4))

# Get the width and height of the camera image
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# JSON file path
json_file_path = "iris_data.json"

# Load existing data from the JSON file
try:
    with open(json_file_path, "r") as json_file:
        json_data = json.load(json_file)
except FileNotFoundError:
    # If the file doesn't exist, initialize an empty dictionary
    json_data = {"circles": [], "left_irises": [], "right_irises": []}




# Create a fullscreen window with five circles at corners and center
cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

cv2.setMouseCallback("Video", mouse_callback)
global rect_color
rect_color = (0, 0, 255)  # Red color

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    circle_radius = 10
    circle_color = (255, 0, 0)  # Blue color

    # Calculate circle positions
    top_left_circle_position = (circle_radius * 2, circle_radius * 2)
    top_center_circle_position = (screen_width // 2, circle_radius * 2)
    top_right_circle_position = (screen_width - circle_radius * 2, circle_radius * 2)
    middle_left_circle_position = (circle_radius * 2, screen_height // 2)
    middle_center_circle_position = (screen_width // 2, screen_height // 2)
    middle_right_circle_position = (
        screen_width - circle_radius * 2,
        screen_height // 2,
    )
    bottom_left_circle_position = (circle_radius * 2, screen_height - circle_radius * 2)
    bottom_center_circle_position = (
        screen_width // 2,
        screen_height - circle_radius * 2,
    )
    bottom_right_circle_position = (
        screen_width - circle_radius * 2,
        screen_height - circle_radius * 2,
    )

    # Draw circles on the frame
    cv2.circle(
        frame, top_center_circle_position, circle_radius, circle_color, -1
    )  # Middle-center
    cv2.circle(
        frame, top_left_circle_position, circle_radius, circle_color, -1
    )  # Top-left
    cv2.circle(
        frame, top_right_circle_position, circle_radius, circle_color, -1
    )  # Top-right
    cv2.circle(
        frame, middle_left_circle_position, circle_radius, circle_color, -1
    )  # Middle-left
    cv2.circle(
        frame, middle_center_circle_position, circle_radius, circle_color, -1
    )  # Middle-center
    cv2.circle(
        frame, middle_right_circle_position, circle_radius, circle_color, -1
    )  # Middle-right
    cv2.circle(
        frame, bottom_left_circle_position, circle_radius, circle_color, -1
    )  # Bottom-left
    cv2.circle(
        frame, bottom_center_circle_position, circle_radius, circle_color, -1
    )  # Bottom-center
    cv2.circle(
        frame, bottom_right_circle_position, circle_radius, circle_color, -1
    )  # Bottom-right

    # Draw a red rectangle at the middle of the frame
    rect_width, rect_height = 180, 280
    rect_start_point = (
        (screen_width - rect_width) // 2,
        (screen_height - rect_height) // 2,
    )
    rect_end_point = (
        (screen_width + rect_width) // 2,
        (screen_height + rect_height) // 2,
    )
    cv2.rectangle(frame, rect_start_point, rect_end_point, rect_color, 2)

    # Detect face and landmarks
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    if len(faces) > 0:
        landmarks = predictor(gray, faces[0])

        # Check if the face is within the red rectangle
        face_x = faces[0].left()
        face_y = faces[0].top()
        if (
            rect_start_point[0] + 10 < face_x < rect_end_point[0] + 10
            and rect_start_point[1] + 10 < face_y < rect_end_point[1] + 10
        ):
            # Face is in the middle, turn the rectangle green
            rect_color = (0, 255, 0)

        else:
            rect_color = (0, 0, 255)

        # Extract eye landmarks
        left_eye_landmarks = [
            (landmarks.part(i).x, landmarks.part(i).y) for i in range(36, 42)
        ]
        right_eye_landmarks = [
            (landmarks.part(i).x, landmarks.part(i).y) for i in range(42, 48)
        ]
        left_eye_pts = np.array(left_eye_landmarks, dtype=np.int32)
        right_eye_pts = np.array(right_eye_landmarks, dtype=np.int32)

        # Draw convex hull around the eyes
        cv2.polylines(frame, [cv2.convexHull(left_eye_pts)], True, (0, 255, 0), 1)
        cv2.polylines(frame, [cv2.convexHull(right_eye_pts)], True, (0, 255, 0), 1)

        left_eye = landmarks.part(36).x, landmarks.part(36).y
        right_eye = landmarks.part(45).x, landmarks.part(45).y

        cv2.circle(frame, left_eye, 2, (255, 255, 255), thickness=1)
        cv2.circle(frame, right_eye, 2, (255, 255, 255), thickness=1)

        left_eye_text = f"Left Eye: ({left_eye[0]}, {left_eye[1]})"
        right_eye_text = f"Right Eye: ({right_eye[0]}, {right_eye[1]})"

        cv2.putText(
            frame,
            left_eye_text,
            (10, 40),
            cv2.FONT_HERSHEY_PLAIN,
            1,
            (255, 255, 255),
            1,
        )
        cv2.putText(
            frame,
            right_eye_text,
            (10, 70),
            cv2.FONT_HERSHEY_PLAIN,
            1,
            (255, 255, 255),
            1,
        )

    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Save the updated data to the JSON file
with open(json_file_path, "w") as json_file:
    json.dump(json_data, json_file, indent=2)

cap.release()
cv2.destroyAllWindows()
