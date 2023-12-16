import cv2
import mediapipe as mp
import json
import dlib
import numpy as np
from keras.models import load_model
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
predictor = dlib.shape_predictor("Test codes\shape_predictor_68_face_landmarks.dat")
face_detector = dlib.get_frontal_face_detector()

detector = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5)
json_file_path = "iris_data.json"

with open(json_file_path, "r") as json_file:
    json_data = json.load(json_file)

screen_width, screen_height = pyautogui.size()
model = load_model("gaze_detection_model.h5")

pyautogui.FAILSAFE = False
cap = cv2.VideoCapture(1)

# Initialize variables for finger clicks
click_threshold = 50  # Adjust the threshold based on your preference
prev_click_state = False
def Cursor_control():
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector(gray)

        if len(faces) > 0:
            landmarks = predictor(gray, faces[0])
            # Extract iris positions
            left_eye = landmarks.part(42).x, landmarks.part(42).y
            right_eye = landmarks.part(45).x, landmarks.part(45).y
            # Control the mouse cursor using gaze prediction
            input_data = np.array([[left_eye[0], left_eye[1], right_eye[0], right_eye[1]]])
            predicted_gaze = model.predict(input_data)[0]
            mouse_x, mouse_y = int(predicted_gaze[0]), int(predicted_gaze[1])
            pyautogui.moveTo(
                mouse_x / frame.shape[1] * screen_width,
                mouse_y / frame.shape[0] * screen_height,
            )

        results = detector.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]

            # Extract finger tip positions
            index_finger_tip = (
                int(
                    hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                    * frame.shape[1]
                ),
                int(
                    hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                    * frame.shape[0]
                ),
            )
            middle_finger_tip = (
                int(
                    hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x
                    * frame.shape[1]
                ),
                int(
                    hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
                    * frame.shape[0]
                ),
            )
            thumb_tip = (
                int(
                    hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
                    * frame.shape[1]
                ),
                int(
                    hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
                    * frame.shape[0]
                ),
            ) 

            # Check finger distances for click actions
            thumb_to_index_distance = np.linalg.norm(
                np.array(thumb_tip) - np.array(index_finger_tip)
            )
            thumb_to_middle_distance = np.linalg.norm(
                np.array(thumb_tip) - np.array(middle_finger_tip)
            )

            # Perform clicks based on finger distances
            if thumb_to_index_distance < click_threshold:
                pyautogui.click(button="left")
            elif thumb_to_middle_distance < click_threshold:
                pyautogui.click(button="right")

        cv2.imshow("Gaze Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release the VideoCapture and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()