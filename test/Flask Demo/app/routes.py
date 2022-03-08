from app import app
from flask import render_template
# import song

# load pickle file

# render default webpage
@app.route('/')
def hello_world():
    return render_template('index.html')

# file upload
# @app.route('/upload')
#def upload():
    # read file contents
    # write file contents to output.wav
    # total = song("output.wav", 0)
    # total.find_key()
    # total.cal_address()
    # idx = total.search()

    # print('Predicted Song {}'.format(allsongs[idx]))
    #pass