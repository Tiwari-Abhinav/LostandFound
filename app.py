import os
import json
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from werkzeug.utils import secure_filename

# Initialize the Flask application
app = Flask(__name__)

# --- Configuration for File Uploads ---
UPLOAD_FOLDER = 'static/uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Configuration for Persistent Data ---
DATA_FILE = 'items.json'

def load_items():
    """Loads items from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_items(items_list):
    """Saves the entire list of items to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(items_list, f, indent=4)

# Load initial data from the file
items = load_items()


@app.route('/')
def index():
    """Renders the main page with a list of all lost and found items."""
    return render_template('index.html', items=reversed(items))

@app.route('/lost', methods=['GET', 'POST'])
def report_lost():
    """Handles the form for reporting a lost item, including image upload."""
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        description = request.form.get('description')
        location = request.form.get('location')
        contact = request.form.get('contact')
        
        image_filename = None
        if 'item_image' in request.files:
            image_file = request.files['item_image']
            if image_file.filename != '':
                image_filename = secure_filename(image_file.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                image_file.save(save_path)

        new_item = {
            'status': 'Lost',
            'name': item_name,
            'description': description,
            'location': location,
            'contact': contact,
            'image_filename': image_filename,
            'timestamp': datetime.now().strftime("%d %b %Y, %I:%M %p")
        }
        items.append(new_item)
        save_items(items)
        return redirect(url_for('index'))

    return render_template('lost.html')

@app.route('/found', methods=['GET', 'POST'])
def report_found():
    """Handles the form for reporting a found item, including image upload."""
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        description = request.form.get('description')
        location = request.form.get('location')
        contact = request.form.get('contact')

        image_filename = None
        if 'item_image' in request.files:
            image_file = request.files['item_image']
            if image_file.filename != '':
                image_filename = secure_filename(image_file.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                image_file.save(save_path)

        new_item = {
            'status': 'Found',
            'name': item_name,
            'description': description,
            'location': location,
            'contact': contact,
            'image_filename': image_filename,
            'timestamp': datetime.now().strftime("%d %b %Y, %I:%M %p")
        }
        items.append(new_item)
        save_items(items)
        return redirect(url_for('index'))

    return render_template('found.html')

# The following block is commented out or removed for production.
# A production server like Gunicorn will import the 'app' object and run it.
# if __name__ == '__main__':
#     app.run(debug=True)

