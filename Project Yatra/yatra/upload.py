import os
import requests

# Define the folder path where the images are stored
folder_path = "C:\\Users\\Lenovo\\Desktop\\food images\\destination images"

# Define the API endpoint URL for your food image model

id=71
# Loop over all image files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        # Construct the full file path

        food_id = os.path.splitext(filename)[0]
        # actual_id=70+int(food_id)
        # Define the path to the image file
        image_path = os.path.join(folder_path, filename)
        
        
        # Open the image file and read its contents
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
            print(image_file)
        
        # Define the parameters for the API request
        params = {
            "destination": food_id,
        }
        files = {
            "image": (f"{food_id}.jpg", image_data)
        }

        
        # Send the API request
        # http://127.0.0.1:8000/api/destination/1/image/create/
        api_url = f"http://127.0.0.1:8000/api/destination/{food_id}/image/create/"
        response = requests.post(api_url, data=params,files=files)
        id+=1
        
        # Check if the API request was successful
        if response.status_code == 200:
            print("Image uploaded successfully:", filename)
        else:
            print("Error uploading image:", filename, response.text)
        
