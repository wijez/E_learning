import os

from dotenv import load_dotenv
import cloudinary

load_dotenv()

def setup_cloudinary():
    cloudinary.config(
        cloud_name=os.getenv('CLOUD_NAME'),
        api_key=os.getenv('API_KEY'),
        api_secret=os.getenv('API_SECRET'),
        secure=True,
        cloudinary_url=os.getenv('CLOUDINARY_URL')
    )


