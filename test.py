import requests
import os   
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

image_url = "https://s.abcnews.com/images/GMA/190919melissablakemain_hpMain_16x9_992.jpg"

url = "https://api-us.faceplusplus.com/facepp/v3/detect"

payload = {
    "api_key": api_key,
    "api_secret": api_secret,
    "image_url": image_url,
    "return_attributes": "beauty,age,gender,emotion"
}

try:
    response = requests.post(url, data=payload)
    response.raise_for_status()  # Raises an HTTPError for bad responses
    result = response.json()

    # print("API Response Status Code:", response.status_code)
    # print("Full API Response:")
    # print(result)

    if 'error_message' in result:
        print(f"API Error: {result['error_message']}")

    elif 'faces' in result and result['faces']:
        face = result['faces'][0]
        beauty_score = face['attributes']['beauty']
        age = face['attributes']['age']
        print(f"Beauty Score: {beauty_score}")
        print(f"Age: {age}")

    else:
        print("No faces detected in the image.")

except requests.exceptions.RequestException as e:
    print(f"Request Error: {e}")
except KeyError as e:
    print(f"KeyError: {e}. This key is missing in the API response.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

