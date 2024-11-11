from flask import Flask, request, render_template
import requests
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
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

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # Prepare API request
            url = "https://api-us.faceplusplus.com/facepp/v3/detect"
            payload = {
                "api_key": api_key,
                "api_secret": api_secret,
                "return_attributes": "beauty,age"
            }
            
            with open(filepath, 'rb') as image_file:
                files = {'image_file': image_file}
                response = requests.post(url, data=payload, files=files)
                response.raise_for_status()
                result = response.json()

            if 'error_message' in result:
                return render_template('result.html', error=result['error_message'])
            
            if not result.get('faces'):
                return render_template('result.html', error="No faces detected in the image.")
                
            face = result['faces'][0]
            return render_template('result.html', 
                                beauty=face['attributes']['beauty'],
                                age=face['attributes']['age'])

        except requests.RequestException as e:
            return render_template('result.html', error=f"API Error: {str(e)}")
        except Exception as e:
            return render_template('result.html', error=f"An error occurred: {str(e)}")
        finally:
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)