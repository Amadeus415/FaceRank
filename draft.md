# Overview - FaceRank webapp
FaceRank is a web application where users upload a photo to receive a beauty score, an improvement score, and tailored product recommendations.

# Tech stack
Backend: Flask (Python)
Frontend: HTML, TailwindCSS for styling
API: Face++ (for beauty scoring)
E-commerce: Amazon products list (possibly through affiliate links for product recommendations)

# Pages & Functionality

## Landing Page (/)
 * Purpose: Introduce the FaceRank service and encourage photo submission.
 * Functionality: Displays a brief explanation of the service, user testimonials, and a photo upload form. Upon photo submission, it redirects to the Results page.

## Results Page (/results)
 * Purpose: Display the beauty score and potential improvement score based on the submitted photo.
 * Functionality: Uses the Face++ API to calculate a score, then displays results to the user with a prompt to improve the score. A link to product recommendations is displayed, leading to the paywall if clicked.

## Paywall Page (/paywall)
 * Purpose: Block access to the product page until payment is made.
 * Functionality: Prompts the user to pay (possibly through Stripe or another payment processor) to access personalized recommendations. Upon payment, the user is redirected to the Product Page.

## Product Page (/products)
* Purpose: Display personalized product recommendations.
* Functionality: Lists products that could help improve the user’s score, linking to Amazon affiliate products. These could include beauty products, skincare items, or grooming tools.


# File Tree

facerank/
├── app/
│   ├── __init__.py                # Initializes the Flask app, loads config, and sets up routes
│   ├── routes.py                  # Defines routes for each page (e.g., landing, results, paywall)
│   ├── forms.py                   # Manages forms and user input validation (e.g., photo uploads)
│   ├── utils.py                   # Utility functions like Face++ API calls, image processing
│   ├── templates/                 # HTML templates for rendering pages
│   │   ├── base.html              # Base layout template (header, footer, etc.)
│   │   ├── landing.html           # Template for the Landing page
│   │   ├── results.html           # Template for the Results page
│   │   ├── paywall.html           # Template for the Paywall page
│   │   └── products.html          # Template for the Product recommendations page
│   ├── static/                    # Static assets such as CSS and JavaScript
│   │   ├── css/
│   │   │   └── tailwind.css       # Tailwind CSS file for page styling
│   │   └── js/
│   │       └── script.js          # JavaScript for interactivity (e.g., form validation)
├── .env                           # Stores environment variables like API keys (e.g., Face++, Stripe)
├── .venv/                         # Python virtual environment directory for dependencies
├── config.py                      # Configuration settings for app, loads from .env file
├── requirements.txt               # List of Python dependencies (e.g., Flask, requests)
├── run.py                         # Entry point to start the Flask app
└── README.md                      # Documentation on how to set up and use the project

Folder & File Explanations
app/ - Main Application Folder
This is the primary folder containing all your app logic, organized into modular files.

__init__.py: Initializes the Flask app by loading configuration and registering routes. Typically, it looks for environment variables and loads them via config.py.

routes.py: Defines routes for each web page:

/ (Landing Page)
/results (Results Page after submitting a photo)
/paywall (Paywall page that blocks access to the Product page)
/products (Product recommendation page)
forms.py: Contains form classes for managing user input, such as the photo upload form. Flask-WTF can help handle validations here.

utils.py: Helper functions to keep code organized. For example:

call_faceplus_api() to send requests to Face++ and process responses.
Functions for formatting beauty score output.
Any image processing or validation logic before the API call.
templates/ - HTML Templates
Contains the HTML files for each page, separated for maintainability and reusability.

base.html: The main layout, defining structure for the app. This file usually contains a header, footer, and block elements like {{ content }} for injecting page-specific content.

Other HTML Files: Each page (Landing, Results, Paywall, Products) has its template. They extend base.html to share the consistent layout and may also include dynamic elements depending on data passed from the routes.

static/ - Static Assets
Contains front-end assets like CSS and JavaScript.

css/tailwind.css: Contains all your custom Tailwind CSS styles, which help define the look and feel of the web app.

js/script.js: Custom JavaScript functions, such as client-side validation or handling interactive elements like modal pop-ups or button actions.

.env - Environment Variables
Used to securely store API keys and sensitive information. Keys are then loaded by config.py to access them in your app.

.venv/ - Virtual Environment
This is where Python dependencies are stored. By using a virtual environment, you ensure all dependencies are contained and avoid version conflicts.

config.py - Configuration Settings
Handles app configuration, often pulling sensitive information from the .env file. Typical configurations include:

python
Copy code
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

class Config:
    FACEPLUS_API_KEY = os.getenv('FACEPLUS_API_KEY')
    FACEPLUS_API_SECRET = os.getenv('FACEPLUS_API_SECRET')
    STRIPE_API_KEY = os.getenv('STRIPE_API_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')  # for Flask-WTF forms

config = Config()
requirements.txt - Python Dependencies
Lists required packages to run the app. For example:

Copy code
Flask
python-dotenv
requests
Flask-WTF
run.py - Entry Point
Contains code to start the Flask app. A simple version might look like this:

python
Copy code
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
README.md - Documentation
Outlines instructions for setting up the project, such as how to install dependencies, run the app, and any environment variables that need to be set in .env.