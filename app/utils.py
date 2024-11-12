import requests
from config import Config

def call_faceplusplus_api(image_stream):
    url = 'https://api-us.faceplusplus.com/facepp/v3/detect'
    files = {'image_file': image_stream}
    data = {
        'api_key': Config.FACEPLUS_API_KEY,
        'api_secret': Config.FACEPLUS_API_SECRET,
        'return_attributes': 'beauty'
    }
    response = requests.post(url, files=files, data=data)
    response.raise_for_status()
    return response.json()
