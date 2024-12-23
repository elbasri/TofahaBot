import requests
import os
from datetime import datetime

# API endpoint for data submission
API_URL = "http://109.205.181.81:5000/api/robot/apples"

# Path to a local image file for testing
IMAGE_PATH = "static/tests/khasra.png"  # Replace with the path to your local test image

# Function to simulate sending data to the API
def simulate_data_submission():
    # Data to simulate
    data = {
        "robot_id": "robot_test_1",
        "tree_id": "tree_test_123",
        "apple_id": "apple_test_456",
        "status": "rotten",  # Simulating a rotten apple
        "timestamp": datetime.now().isoformat()
    }

    # Prepare the files payload if an image is available
    files = {"image": open(IMAGE_PATH, "rb")} if os.path.exists(IMAGE_PATH) else None

    try:
        # Send POST request to the API
        response = requests.post(API_URL, data=data, files=files)

        # Handle the response
        if response.status_code == 200:
            print("Data submitted successfully:", response.json())
        else:
            print("Failed to submit data:", response.status_code, response.text)
    except Exception as e:
        print("An error occurred while sending data:", str(e))

# Run the simulation
if __name__ == "__main__":
    simulate_data_submission()
