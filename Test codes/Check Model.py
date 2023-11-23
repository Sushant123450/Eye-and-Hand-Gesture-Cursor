import numpy as np
import cv2
import dlib
import json
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential, load_model

# Load the pre-trained face detector and shape predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("Test codes\shape_predictor_68_face_landmarks.dat")

# JSON file path
json_file_path = "Test codes\iris_data.json"

# Load data from the JSON file
with open(json_file_path, "r") as json_file:
    json_data = json.load(json_file)

# # Extract features (iris positions) and labels (circle positions)
# iris_left = np.array(json_data["left_irises"])
# iris_right = np.array(json_data["right_irises"])
# circles = np.array(json_data["circles"])

# # Combine left and right iris positions
# iris_positions = np.concatenate((iris_left, iris_right), axis=1)

# # Combine iris positions and circles to form the feature matrix
# features = np.concatenate((iris_positions, circles), axis=1)

# # Normalize features to be in the range [0, 1]
# features = features / np.array([screen_width, screen_height, screen_width, screen_height])

# # Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(features, iris_positions, test_size=0.2, random_state=42)

# Load the trained model
model = load_model("Test codes\gaze_detection_model.h5")

# Create a VideoCapture object
cap = cv2.VideoCapture(0)

Sensitivity = int(input("Sensitivty="))

# Get the screen width and height
screen_width = int(cap.get(3))
screen_height = int(cap.get(4))

while True:
    ret, frame = cap.read()

    # Detect face and landmarks
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    if len(faces) > 0:
        landmarks = predictor(gray, faces[0])

        # Extract iris positions
        left_eye = landmarks.part(42).x, landmarks.part(42).y
        right_eye = landmarks.part(45).x, landmarks.part(45).y

        # Combine iris positions and circles to form the input for the model
        input_data = np.array([[left_eye[0], left_eye[1], right_eye[0], right_eye[1]]])
        input_data = input_data / np.array(
            [screen_width, screen_height, screen_width, screen_height]
        )

        # Predict gaze position
        predicted_gaze = model.predict(input_data)[0]

        # Scale the predicted gaze position back to screen coordinates
        predicted_gaze = predicted_gaze * np.array(
            [screen_width * Sensitivity, screen_height * Sensitivity]
        )
        print(int(predicted_gaze[0]), int(predicted_gaze[1]))
        # Draw a circle at the predicted gaze position
        gaze_radius = 5
        gaze_color = (0, 0, 255)  # Red color
        cv2.circle(
            frame,
            (int(predicted_gaze[0]), int(predicted_gaze[1])),
            gaze_radius,
            gaze_color,
            -1,
        )

    # Display the frame
    cv2.imshow("Gaze Tracking", frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the VideoCapture and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
# import numpy as np
# import cv2
# import dlib
# import json
# from tensorflow.keras.models import load_model
# import pygetwindow as gw
# import pyautogui

# # Load the pre-trained face detector and shape predictor
# detector = dlib.get_frontal_face_detector()
# predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# pyautogui.FAILSAFE(False)
# # Load the trained model
# model = load_model("gaze_detection_model.h5")

# # Get the screen resolution
# # screen = gw.getWindowsWithTitle()[0]q
# screen_width =  1920 #screen.width
# screen_height = 1080 #screen.height

# # Create a VideoCapture object
# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()

#     # Detect face and landmarks
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = detector(gray)

#     if len(faces) > 0:
#         landmarks = predictor(gray, faces[0])

#         # Extract iris positions
#         left_eye = landmarks.part(42).x, landmarks.part(42).y
#         right_eye = landmarks.part(45).x, landmarks.part(45).y

#         # Combine iris positions to form the input for the model
#         input_data = np.array([[left_eye[0], left_eye[1], right_eye[0], right_eye[1]]])

#         # Predict gaze position
#         predicted_gaze = model.predict(input_data)[0]

#         # Scale the predicted gaze position to match the screen resolution
#         predicted_gaze = predicted_gaze * np.array([1920, 1080])

#         # Draw a circle at the predicted gaze position on the desktop
#         dot_radius = 5
#         dot_color = (0, 0, 255)  # Red color
#         dot_position = (int(predicted_gaze[0] + 960), int(predicted_gaze[1] - 540))

#         # Move the mouse smoothly to the predicted gaze position
#         pyautogui.moveTo(dot_position[0], dot_position[1], duration=0.25)

#     # Break the loop if 'q' key is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the VideoCapture and close the OpenCV window
# cap.release()
# cv2.destroyAllWindows()
