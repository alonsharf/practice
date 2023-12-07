import os

import requests


def publish_package(directory):
    
    # Set the URL to which you want to send the file
    url = f"url-{directory}/"
    headers = {
        'Content-Type': 'multipart/form-data'
    }
    if os.listdir(directory):
        files = os.listdir(directory)
        for file in files:
            file_path = os.path.join(directory, file)
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(url, files=files, headers=headers ,auth=("username", "password"))
                if response.status_code == 201:
                    print(f"File {file} uploaded successfully")
                    os.remove(file_path)
                else:
                    print(f"Failed to upload {file}, Response {response.text}")
                    os.remove(file_path)


def main():

    # Iterate over each directory and upload packages
    directories = ['focal', 'bionic', 'jammy']
    for directory in directories:
        publish_package(directory)