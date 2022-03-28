import os
from app import app
from flask import render_template, jsonify, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

# from app import imports
# from app import pickleFileCode
# from app import songFileCode
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

    #     return render_template('index.html', request="POST")
    # else:
    #     return render_template("index.html")
    # if request.method == 'POST':
    #     print("Recieved Audio File")
    #     print(request.files)
    #     # check if the post request has the file part
    #     if 'file' not in request.files:
    #     # if 'file' not in request.files['audio_data']:
    #         return jsonify({"error" : "No file part"})

    #     file = request.files['file']
    #     # file = request.files['audio_data']
    #     print("file")
    #     # If the user does not select a file, the browser submits an
    #     # empty file without a filename.
    #     if file.filename == '':
    #         return jsonify({"error" : "No selected file"})

    #     if file and not allowed_file(file.filename):
    #         return jsonify({"error" : "No selected file"})

    #     print("Upload filename = " + file.filename)
    #     filename = secure_filename(file.filename)
    #     filepath = os.path.join(UPLOAD_FOLDER, filename)
    #     file.save(filepath)

    #     prediction = model.predict(filepath)
    #     # prediction = model.predict()
    #     return jsonify(prediction)


# import song

# load pickle file

# render default webpage
# @app.route('/')
# def hello_world():
#     return render_template('index.html')

@app.route("/", methods=['POST', 'GET'])
def index():
    # if request.method == "POST":
    #     f = request.files['audio_data']
    #     with open('audio.wav', 'wb') as audio:
    #         f.save(audio)
    #     print('file uploaded successfully')

    #     return render_template('index.html', request="POST")
    # else:
    #     return render_template("index.html")
    return render_template('index.html')

@app.route('/predict')
def predict():
    prediction = model.predict()
    return jsonify(prediction)

# file upload
# @app.route('/upload')
# def upload():
    # audio_input = request.files['file']
    # response = speechAPI.get_translation(audio_input)
    # audio_input = request.files['file']
    # response = (audio_input)
    # return (response)
    # return jsonify(response)

    # read file contents
    # write file contents to output.wav
    # total = song("output.wav", 0)
    # total.find_key()
    # total.cal_address()
    # idx = total.search()

    # print('Predicted Song {}'.format(allsongs[idx]))

    # remove_wav = (allsongs[idx]).replace('.wav', '')
    # predicted_song = remove_wav.replace(' ', '%20')
    # print(predicted_song)

    # youtube_link = "https://www.youtube.com/results?search_query="
    # youtube_song_link = "".join((youtube_link, predicted_song))
    # print("Youtube Lesson - " + youtube_song_link +"%20guitar%20lesson")

    # guitar_tab_link = "https://www.ultimate-guitar.com/search.php?search_type=title&value="
    # guitar_tab_song_link = "".join((guitar_tab_link, predicted_song))
    # print("Guitar Tab - " + guitar_tab_song_link)
    #pass