from flask import Flask, config, render_template, flash, request, redirect,url_for
from werkzeug.utils import secure_filename
import os
import src.annoy_search as ann
import sqlite3
from flask import g
import src.db_util as dbutil

import src.config as config


app = Flask(__name__)
app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = config.IMAGES_UPLOAD_PATH
app.config['USER_UPLOAD_FOLDER'] = config.USER_UPLOAD_FOLDER
app.config['USER_SEARCH_IMAGE'] = config.USER_SEARCH_IMAGE


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST', 'GET'])
def index():
    images = dbutil.get_image_from_database([])
    return render_template('index.html', images=images)

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['USER_UPLOAD_FOLDER'], filename))
            flash('Image successfully uploaded and displayed below')
            return render_template('upload.html', filename=filename)
        else:
            flash('Allowed image types are -> png, jpg, jpeg')
            return redirect(request.url)
    else:
        return render_template("upload.html")

@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_saved_path = os.path.join(app.config['USER_SEARCH_IMAGE'], filename)
            file.save(file_saved_path)
            flash('Image successfully uploaded, looking for similar images')
            ids = ann.image_search(file_saved_path)
            images = dbutil.get_image_from_database(ids)
            return render_template('index.html', images=images)
        else:
            flash('Allowed image types are -> png, jpg, jpeg')
            return redirect(request.url)
    else:
        ids = ann.text_search(request.args['search'])
        images = dbutil.get_image_from_database(ids)
        return render_template('index.html', images=images)

if __name__ == '__main__':
    os.makedirs(config.IMAGES_UPLOAD_PATH, exist_ok=True) # not good a good idea for production
    app.run(debug=True, host='0.0.0.0', port=5050)