import numpy as np
import json
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

def Train_Model():
    json_file_path = "iris_data.json"
    with open(json_file_path, "r") as json_file:
        json_data = json.load(json_file)

    # Extract features (iris positions) and labels (circle positions)
    iris_left = np.array([(point["x"], point["y"]) for point in json_data["left_irises"]])
    iris_right = np.array([(point["x"], point["y"]) for point in json_data["right_irises"]])
    circles = np.array([(point["x"], point["y"]) for point in json_data["circles"]])

    # Stack iris positions vertically
    iris_positions = np.concatenate((iris_left, iris_right), axis=1)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(iris_positions, circles, test_size=0.2, random_state=42)

    # Define the neural network model
    model = Sequential()
    model.add(Dense(64, activation='relu', input_shape=(4,)))
    model.add(Dense(64, activation='linear'))
    model.add(Dense(2, activation='relu'))  # Output layer with 2 neurons for x and y coordinates

    # Compile the model with Adam optimizer and mean sq     uared error loss
    model.compile(optimizer=Adam(), loss='mean_squared_error')

    # Train the model
    model.fit(X_train, y_train, epochs=300, batch_size=32, validation_data=(X_test, y_test))

    # Evaluate the model on the test set
    loss = model.evaluate(X_test, y_test)
    print(f"Test Loss: {loss}")
    model.save("gaze_detection_model.h5")
