# Music-Recongnition-Tab

## Setup
First make sure your device has the following Python libraries:
* import wave
* import numpy as np
* import matplotlib.pyplot as plt
* import matplotlib.mlab as mlab
* from scipy import signal
* import seaborn as sns
* from scipy.io import wavfile
* import pylab
* import matplotlib.mlab as ml
* from scipy.fftpack import fft
* import pickle
* import os
* %matplotlib tk

After your device has these libraries, download both the **hashtable and songid pickle files**, next create a folder called **Song_Wav** and add 6 wav files of songs you wish to identify.
Next create a text file call **songs** and add one per line the name of the wav files, for example *Title - Artist.wav*, with the last song added to the text file leave a space after the word wav.
After these files and folders have been created use the code from **server_side.ipynb** in Jupyter Notebook and run the code to create the database for the application.

Next download the **Flask App**, replace the **hashtable and songid pickle files and songs.txt file** from the app folder in Flask with the newly made ones.
Open the Flask App fodler in a coding enviroment like VSCode, using the terminal do the following:
* Type *py -3 -m venv .venv*
* .venv\scripts\activate
* Open command palette and choose the most upto date Python Interpreter with .venv in it
* Then run *python -m pip install flask* if Flask in not installed on your device
* Last run *python -m flask run* or used *flask run*

## Resources
* Most Helpful - https://github.com/KavyaVarma/Music-Recognition
* https://stackoverflow.com/questions/66310336/how-to-print-the-output-of-flask-function-in-a-pop-up-box-in-html
* https://stackoverflow.com/questions/60226359/how-to-retrieve-data-as-file-object-on-flask-webserver
* https://stackoverflow.com/questions/57443543/display-prediction-on-a-webpage-through-flask
* https://medium.com/star-gazers/building-churn-predictor-with-python-flask-html-and-css-fbab760e8441
* https://towardsdatascience.com/model-deployment-using-flask-c5dcbb6499c9
* https://towardsdatascience.com/building-a-machine-learning-web-application-using-flask-29fa9ea11dac
* https://iq.opengenus.org/web-app-ml-model-using-flask/
* https://codeutility.org/python-displaying-json-in-the-html-using-flask-and-local-json-file-stack-overflow/
* https://datatables.net/forums/discussion/50315/how-to-use-flask-framework-to-render-the-html-send-json-data-and-have-ajax-update-table
* https://joseph-dougal.medium.com/flask-ajax-bootstrap-tables-9036410cbc8
* https://developers.google.com/web/fundamentals/media/recording-audio
* https://medium.com/jeremy-gottfrieds-tech-blog/javascript-tutorial-record-audio-and-encode-it-to-mp3-2eedcd466e78
* https://developer.mozilla.org/en-US/docs/Web/API/MediaStream_Recording_API/Using_the_MediaStream_Recording_API
* https://developer.mozilla.org/en-US/docs/Web/API/MediaStream_Recording_API
* https://www.codegrepper.com/code-examples/javascript/save+mediastream+to+file
* https://howtocreateapps.com/fetch-and-display-json-html-javascript/
* https://stackoverflow.com/questions/883977/display-json-as-html
* https://developer.mozilla.org/en-US/docs/Web/API/MediaStream_Recording_API/Using_the_MediaStream_Recording_API
* https://javascript.tutorialink.com/send-wav-file-from-js-to-flask/
* Most Helpful - https://blog.addpipe.com/using-recorder-js-to-capture-wav-audio-in-your-html5-web-site/
