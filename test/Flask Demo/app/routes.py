from app import app
from flask import render_template

# from app import imports
# from app import pickleFileCode
# from app import songFileCode
from app import model
# import song

# load pickle file

# render default webpage
@app.route('/')
def hello_world():
    return render_template('index.html')

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