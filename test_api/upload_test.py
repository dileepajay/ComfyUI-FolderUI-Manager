import requests

# Define the API endpoint
url = "http://127.0.0.1:8188/folderui/upload"

# Define the file path to upload
file_path = r"C:\\Users\\medre\\OneDrive\\Desktop\\aaa.png"

# Open the file in binary mode and send the request
with open(file_path, "rb") as file:
    files = {"file": (file_path.split("\\")[-1], file, "image/png")}
    data = {"type":"input","imagepath": "rmbg/aaa_.png"}  # Define where to save the file in the API

    response = requests.post(url, files=files, data=data)

# Print the response
print(response.status_code)
print(response.json())