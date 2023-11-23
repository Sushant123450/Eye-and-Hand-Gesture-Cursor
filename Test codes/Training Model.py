import numpy as np
import cv2
import json
import platform
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Function to get screen width and height
def get_screen_dimensions():
    screen_width, screen_height = 1920, 1080  # Default values (replace with actual dimensions)
    if platform.system() == "Windows":
        try:
            import ctypes
            user32 = ctypes.windll.user32
            screen_width = user32.GetSystemMetrics(0)
            screen_height = user32.GetSystemMetrics(1)
        except:
            pass
    elif platform.system() == "Linux":
        try:
            from Xlib import display
            screen = display.Display().screen()
            screen_width = screen.width_in_pixels
            screen_height = screen.height_in_pixels
        except ImportError:
            pass
    return screen_width, screen_height

# JSON file path
json_file_path = "Test codes\iris_data.json"

# Load data from the JSON file
with open(json_file_path, "r") as json_file:
    json_data = json.load(json_file)

# Extract features (iris positions) and labels (circle positions)
iris_left = np.array([(point["x"], point["y"]) for point in json_data["left_irises"]])
iris_right = np.array([(point["x"], point["y"]) for point in json_data["right_irises"]])
circles = np.array([(point["x"], point["y"]) for point in json_data["circles"]])

# Stack iris positions vertically
iris_positions = np.concatenate((iris_left, iris_right), axis=1)

# Combine iris positions and circles to form the feature matrix
features = np.concatenate((iris_positions, circles), axis=1)

# Normalize features to be in the range [0, 1]
screen_width, screen_height = get_screen_dimensions()
features = features / np.array([screen_width, screen_height, screen_width, screen_height, screen_width, screen_height])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(iris_positions, circles, test_size=0.2, random_state=42)

# Define the neural network model
model = Sequential()
model.add(Dense(64, activation='relu', input_shape=(4,)))
model.add(Dense(32, activation='relu'))
model.add(Dense(2, activation='linear'))  # Output layer with 2 neurons for x and y coordinates

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Evaluate the model on the test set
loss = model.evaluate(X_test, y_test)
print(f"Test Loss: {loss}")

# Save the trained model
model.save("gaze_detection_model.h5")
