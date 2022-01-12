from flask import Flask, config, render_template, flash, request, redirect,url_for
from werkzeug.utils import secure_filename
import os
import src.anny_search as ann
import sqlite3
from flask import g

import src.config as config


app = Flask(__name__)
app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = config.IMAGES_UPLOAD_PATH
app.config['USER_UPLOAD_FOLDER'] = config.USER_UPLOAD_FOLDER
app.config['USER_SEARCH_IMAGE'] = config.USER_SEARCH_IMAGE


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(config.DATABASE_PATH)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST', 'GET'])
def index():
    images = query_db('SELECT * FROM images limit 16')
    return render_template('index.html', images=images)

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
    print(filename)
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
            #print('upload_image filename: ' + filename)
            flash('Image successfully uploaded and displayed below')
            return render_template('upload.html', filename=filename)
        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect(request.url)
    else:
        return render_template("upload.html")

@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        print('processing post search')
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
            #print('upload_image filename: ' + filename)
            flash('Image successfully uploaded and displayed below')
            print(file_saved_path)
            ids = ann.image_search(file_saved_path)
            images = query_db('SELECT * FROM images WHERE id IN ({})'.format(','.join(map(str, ids))))    
            return render_template('index.html', images=images)
        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect(request.url)
    else:
        ids = ann.text_search(request.args['search'])
        images = query_db('SELECT * FROM images WHERE id IN ({})'.format(','.join(map(str, ids))))
        return render_template('index.html', images=images)

if __name__ == '__main__':
    os.makedirs(config.IMAGES_UPLOAD_PATH, exist_ok=True)
    app.run(debug=True)