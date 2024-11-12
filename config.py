import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    FACEPLUS_API_KEY = os.getenv('FACEPLUS_API_KEY')
    FACEPLUS_API_SECRET = os.getenv('FACEPLUS_API_SECRET')
    STRIPE_API_KEY = os.getenv('STRIPE_API_KEY')
