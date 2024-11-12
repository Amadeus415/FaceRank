from flask import Blueprint, render_template, redirect, url_for, request, session
from .forms import PhotoUploadForm
from .utils import call_faceplusplus_api
import os

# Create uploads directory if it doesn't exist
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Create blueprint
main_bp = Blueprint('main', __name__)

# Landing Page Route
@main_bp.route('/', methods=['GET', 'POST'])
def landing():
    form = PhotoUploadForm()
    if form.validate_on_submit():
        photo = form.photo.data
        photo_path = os.path.join('uploads', photo.filename)
        photo.save(photo_path)
        with open(photo_path, 'rb') as image_stream:
            api_result = call_faceplusplus_api(image_stream)
        # Extract beauty score
        beauty_score = api_result['faces'][0]['attributes']['beauty']['female_score']
        # Store score in session or pass via query params
        session['beauty_score'] = beauty_score
        return redirect(url_for('main.results'))
    return render_template('landing.html', form=form)

# Results Page Route
@main_bp.route('/results')
def results():
    beauty_score = session.get('beauty_score', None)
    if beauty_score is None:
        return redirect(url_for('main.landing'))
    return render_template('results.html', beauty_score=beauty_score)

# Paywall Route
@main_bp.route('/paywall', methods=['GET', 'POST'])
def paywall():
    # Implement payment processing
    # On success:
    return redirect(url_for('main.products'))

# Products Route
@main_bp.route('/products')
def products():
    # Sample product list
    product_list = [
        {'name': 'Garmin Epix', 'description': 'Sports Watch', 'price': 399.99},
        {'name': 'Beef Tallow Moisturizer', 'description': 'All natural moisturizer', 'price': 29.99},
        {'name': 'Shilajit Resin', 'description': 'All natural moisturizer', 'price': 19.99}
    ]
    return render_template('products.html', products=product_list)

