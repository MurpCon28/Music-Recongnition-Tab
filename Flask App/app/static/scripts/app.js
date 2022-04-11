//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream;                      //stream from getUserMedia()
var rec;                            //Recorder.js object
var input;                          //MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb. 
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //audio context to help us record

var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");
var pauseButton = document.getElementById("pauseButton");

//Events have been given to these buttons
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
pauseButton.addEventListener("click", pauseRecording);

function pauseRecording(){
    console.log("pauseButton clicked rec.recording=",rec.recording );
    if (rec.recording){
        //pause
        rec.stop();
        pauseButton.innerHTML="Resume";
    }else{
        //resume
        rec.record()
        pauseButton.innerHTML="Pause";

    }
}

function stopRecording() {
    console.log("stopButton clicked");

    //Stop button is disabled, record button is enabled allowing new recordings
    stopButton.disabled = true;
    recordButton.disabled = false;
    pauseButton.disabled = true;

    //If the recording is paused the reset button can be pressed to rerecord
    pauseButton.innerHTML="Pause";

    //Recorder is told to stop
    rec.stop();

    //Microphone access is stopped
    gumStream.getAudioTracks()[0].stop();

    //Wav blob created and passed into createDownloadLink
    rec.exportWAV(createDownloadLink);
}

function startRecording() {
    console.log("recordButton clicked");

    //Constraint object telling the recording to use audio not video
    var constraints = { audio: true, video:false }

    //Record button is disabled until getUserMedia() returns a success or fail response
    recordButton.disabled = true;
    stopButton.disabled = false;
    pauseButton.disabled = false

    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
        console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

        /*
            After getUserMedia() is called an audioContext is created
            sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
            the sampleRate defaults to the one set in your OS for your playback device

        */

        audioContext = new AudioContext();

        //update the format 
        document.getElementById("formats").innerHTML="Format: 1 channel pcm @ "+audioContext.sampleRate/1000+"kHz"

        //stream = p.open(format=format,channels=channels,rate=rate,input=True,frames_per_buffer=chunk)

        //gumStream is assigned for later use
        gumStream = stream;

        //Stream is used
        input = audioContext.createMediaStreamSource(stream);

        //Recorder object is created and configured to record mono sound, which is 1 channel. Recording 2 channels doubles the file size
        rec = new Recorder(input,{numChannels:1})

        //start the recording process
        rec.record()

        console.log("Recording started");

        //Recording is set to stop after 20 seconds
        setTimeout(stopRecording, 21 * 1000);

    }).catch(function(err) {
        //If getUserMedia() fails the record button is enabled
        recordButton.disabled = false;
        stopButton.disabled = true;
        pauseButton.disabled = true
    });
}

function createDownloadLink(blob) {

    var url = URL.createObjectURL(blob);
    var au = document.createElement('audio');
    var li = document.createElement('li');
    var link = document.createElement('a');

    //filename contains the .wav file that is used for upload and download
    var filename = "audio_file.wav";

    //Controls are added to the audio element 
    au.controls = true;
    au.src = url;

    //save to disk link
    link.href = url;
    link.download = filename; //Forces the browers to download the file from filename
    link.innerHTML = "Save to disk";

    //New audio element is added to li
    li.appendChild(au);

    //filename is added to the li
    li.appendChild(document.createTextNode(filename))

    //Save to disk is added to the li
    li.appendChild(link);

    //upload link
    var upload = document.createElement('a');
    upload.href="#";
    upload.innerHTML = "Upload";
    upload.addEventListener("click", function(event){
          var xhr=new XMLHttpRequest();
          //Displays the reponse prediction from the model
          xhr.onload=function(e) {
              if(this.readyState === 4) {
                  console.log("Server returned: ",e.target.responseText);
                  //const jsonfile = JSON.stringify('{{jsonfile | tojson}}');
                  //const jsonfile = JSON.parse('{{jsonfile | tojson}}');
                  //const jsonfile = JSON.parse(JSON.stringify(jsonfile));
                  //document.querySelector("#result").innerHTML = JSON.stringify(jsonfile, null, 2)
                  //document.getElementById("result").innerHTML = jsonfile;
                  //document.getElementById("result").innerHTML = jsonfile.remove_wav + "<br>" + jsonfile.youtube_song_link + "<br>" + jsonfile.guitar_tab_song_link;
                  document.getElementById("result").innerHTML = e.target.response;
              }
          };
          var fd=new FormData();
          fd.append("audio_data",blob, filename);
          xhr.open("POST","/upload_blob",true);
          xhr.send(fd);
    })
    li.appendChild(document.createTextNode (" ")) //Add a space in between
    li.appendChild(upload) //Add the upload link to li

    //add the li element to the ol
    recordingsList.appendChild(li);
}

//Attempts at tryign to display the results of the predicted song

// function result() {
//     var xhr = new XMLHttpRequest();
//     xhr.open("POST", "/upload_blob"); 
//     xhr.onload = function(event){ 
//         alert("Success, server responded with: " + event.target.response); // raw response in alert popup
//         document.getElementById("song").innerHTML = event.target.response; // set content of the div with id "song" to the server response.
//     }; 
//     // or onerror, onabort
//     var formData = new FormData(document.getElementById("result")); 
//     xhr.send(formData);
// }

//https://stackoverflow.com/questions/66310336/how-to-print-the-output-of-flask-function-in-a-pop-up-box-in-html
//https://stackoverflow.com/questions/60226359/how-to-retrieve-data-as-file-object-on-flask-webserver

//https://stackoverflow.com/questions/57443543/display-prediction-on-a-webpage-through-flask
//https://medium.com/star-gazers/building-churn-predictor-with-python-flask-html-and-css-fbab760e8441
//https://towardsdatascience.com/model-deployment-using-flask-c5dcbb6499c9
//https://towardsdatascience.com/building-a-machine-learning-web-application-using-flask-29fa9ea11dac
//https://iq.opengenus.org/web-app-ml-model-using-flask/

// function results() {
//     // const jsonfile = JSON.parse({{jsonfile|tojson}});
//     const jsonfile = JSON.parse('{{jsonfile | tojson}}');
//     console.log(jsonfile);
//     // const jsonfile = JSON.parse(jsonfile);
//     // document.getElementById("result").innerHTML = jsonfile.prediction + "<br>" + jsonfile.youTube + "<br>" + jsonfile.guitar;
//     //document.getElementById("result").innerHTML = jsonfile.prediction + " " + jsonfile.youTube + " " + jsonfile.guitar;
//     // var jsonStr = JSON.stringify(jsonfile)
//     // document.getElementById("result").innerHTML = jsonStr;
//     document.querySelector("result").innerHTML = JSON.stringify(jsonfile.prediction, jsonfile.youTube, jsonfile.guitar, null, 3);
//     // const prediction = JSON.parse('{{prediction | tojson}}');
//     // console.log(prediction);
//     // document.querySelector("#result").innerHTML = JSON.stringify(jsonfile, null, 2);
// }

    // const jsonfile = JSON.parse({jsonfile,tojson});
    // console.log(jsonfile);
    // document.querySelector("result").innerHTML = JSON.stringify(jsonfile, null, 2);

//https://codeutility.org/python-displaying-json-in-the-html-using-flask-and-local-json-file-stack-overflow/
//https://datatables.net/forums/discussion/50315/how-to-use-flask-framework-to-render-the-html-send-json-data-and-have-ajax-update-table
//https://joseph-dougal.medium.com/flask-ajax-bootstrap-tables-9036410cbc8


// fetch('/upload_blob').then(function(res) {
//     return res.json()
//   }).then(function(json) {
//     const p = document.querySelector('p')
//     const a = document.querySelector('a')
//     // Use the JSON data to populate these elements
//     p.innerHTML = json.Prediction 
//     a.innerHTML = json.YouTube
//     a.innerHTML = json.Guitar

//   }).catch(function(err) {
//     console.log(err.message)
//   })