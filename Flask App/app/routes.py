import os
from app import app
from flask import render_template, jsonify, request, redirect, url_for, flash
import json
from werkzeug.utils import secure_filename
from app import model

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print("Upload filename = " + file.filename)
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            prediction = model.predict(filepath)
            # prediction = model.predict()
            return jsonify(prediction)

            #return render_template('upload.html', prediction=prediction)
        #return render_template('upload.html')
            
            # return redirect(url_for('download_file', name=filename))
            # return jsonify({
            #     "filename" : filename
            # })
    return render_template('upload.html')

@app.route('/upload_blob', methods=['GET', 'POST'])
def upload_blob():
    print("request")
    if request.method == 'POST':
        print("Recieved Audio File")
        print(request.files)
        if 'audio_data' not in request.files:
            return jsonify({"error" : "No file part"})

        file = request.files['audio_data']
        # with open('audio.wav', 'wb') as audio:
        #     file.save(audio)

        if file.filename == '':
            return jsonify({"error" : "No selected file"})

        if file and not allowed_file(file.filename):
            return jsonify({"error" : "No selected file"})
        print('file uploaded successfully')

        print("Upload filename = " + file.filename)
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        prediction = model.predict(filepath)
        # prediction = model.predict()
        return jsonify(prediction)
        # return render_template('index.html', jsonfile=json.dumps(prediction))
        #return render_template('index.html', song=prediction)
    #return render_template('index.html')

@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template('index.html')

# @app.route('/predict')
# def predict():
#     prediction = model.predict()
#     return jsonify(prediction)