import numpy as np
import cv2
import dlib
import json
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential, load_model

# Load the pre-trained face detector and shape predictor
def activate():
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("Test codes\shape_predictor_68_face_landmarks.dat")

    json_file_path = "iris_data.json"
    with open(json_file_path, "r") as json_file:
        json_data = json.load(json_file)

    # Load the trained model
    model = load_model("gaze_detection_model.h5")

    # Create a VideoCapture object
    cap = cv2.VideoCapture(1)
    cv2.namedWindow("Gaze Tracking", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Gaze Tracking", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        # Detect face and landmarks
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        if len(faces) > 0:
            landmarks = predictor(gray, faces[0])

            # Extract iris positions
            left_eye = landmarks.part(42).x, landmarks.part(42).y
            right_eye = landmarks.part(45).x, landmarks.part(45).y

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

            input_data = np.array([[left_eye[0], left_eye[1], right_eye[0], right_eye[1]]])

            # Predict gaze position
            predicted_gaze = model.predict(input_data)[0]

            print(int(predicted_gaze[0]), int(predicted_gaze[1]))
            
            # Draw a circle at the predicted gaze position
            gaze_radius = 5
            gaze_color = (0, 0, 255)  # Red color
            cv2.circle(
                frame,
                # (10,27),
                (int(predicted_gaze[0]), int(predicted_gaze[1])),
                gaze_radius,
                gaze_color,
                -1,
            )

        cv2.imshow("Gaze Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release the VideoCapture and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()