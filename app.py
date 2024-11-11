from flask import Flask, request, render_template
import requests
import os
from dotenv import load_dotenv
import base64
import io


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Get API credentials from environment variables
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file has been uploaded
        if 'photo' not in request.files:
            return render_template('result.html', error="No file part")
        
        file = request.files['photo']
        if file.filename == '':
            return render_template('result.html', error="No selected file")
            
        if not allowed_file(file.filename):
            return render_template('result.html', error="Invalid file type")

        try:
            # Read the file content and seek to the beginning
            file_bytes = file.read()
            
            # Create a copy of the file bytes for the API request
            file_for_api = io.BytesIO(file_bytes)
            
            # Convert to base64 for displaying
            image_b64 = base64.b64encode(file_bytes).decode('utf-8')
            
            # Prepare API request
            url = "https://api-us.faceplusplus.com/facepp/v3/detect"
            payload = {
                "api_key": api_key,
                "api_secret": api_secret,
                "return_attributes": "beauty,age"
            }
            
            # Create the files dict for the API request
            files = {'image_file': ('image.jpg', file_for_api, 'image/jpeg')}
            
            response = requests.post(url, data=payload, files=files)
            response.raise_for_status()
            result = response.json()

            if 'error_message' in result:
                return render_template('result.html', error=result['error_message'])
            
            if not result.get('faces'):
                return render_template('result.html', error="No faces detected in the image.")
                
            face = result['faces'][0]
            
            # Make sure to include the correct MIME type in the data URL
            mime_type = file.content_type or 'image/jpeg'
            image_data_url = f"data:{mime_type};base64,{image_b64}"
            
            return render_template('result.html', 
                                beauty=face['attributes']['beauty'],
                                age=face['attributes']['age'],
                                image_data=image_data_url)

        except requests.RequestException as e:
            return render_template('result.html', error=f"API Error: {str(e)}")
        except Exception as e:
            return render_template('result.html', error=f"An error occurred: {str(e)}")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)