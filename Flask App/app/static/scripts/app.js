//https://developer.mozilla.org/en-US/docs/Web/API/MediaStream_Recording_API/Using_the_MediaStream_Recording_API
//https://javascript.tutorialink.com/send-wav-file-from-js-to-flask/
//https://blog.addpipe.com/using-recorder-js-to-capture-wav-audio-in-your-html5-web-site/

const record = document.querySelector('.record');
const stop = document.querySelector('.stop');
const soundClips = document.querySelector('.sound-clips');
const canvas = document.querySelector('.visualizer');
const mainSection = document.querySelector('.main-controls');

// disable stop button while not recording

stop.disabled = true;

// visualiser setup - create web audio api context and canvas

let audioCtx;
const canvasCtx = canvas.getContext("2d");

//main block for doing the audio recording

if (navigator.mediaDevices.getUserMedia) {
  console.log('getUserMedia supported.');

  const constraints = { audio: true };
  let chunks = [];

  let onSuccess = function(stream) {
    const mediaRecorder = new MediaRecorder(stream);

    visualize(stream);

    let stopRecording = function() {
      mediaRecorder.stop();
      console.log(mediaRecorder.state);
      console.log("recorder stopped");
      record.style.background = "";
      record.style.color = "";
      // mediaRecorder.requestData();

      stop.disabled = true;
      record.disabled = false;

      //record.exportWAV(createDownloadLink);
      // createDownloadLink();
      // createAudioElement();

      // get recorded file
      // upload recorded file to web application
      // display response
    }

    record.onclick = function() {
      mediaRecorder.start();
      console.log(mediaRecorder.state);
      console.log("recorder started");
      record.style.background = "red";

      stop.disabled = false;
      record.disabled = true;

      setTimeout(stopRecording, 20 * 1000);
    }

    stop.onclick = stopRecording;

    mediaRecorder.onstop = function(e) {
      console.log("data available after MediaRecorder.stop() called.");

      const clipName = prompt('Enter a name for your sound clip?','Untitled');

      const clipContainer = document.createElement('article');
      const clipLabel = document.createElement('p');
      const audio = document.createElement('audio');
      const deleteButton = document.createElement('button');
      const downloadLink = document.createElement('link');

      clipContainer.classList.add('clip');
      audio.setAttribute('controls', '');
      deleteButton.textContent = 'Delete';
      deleteButton.className = 'delete';

      downloadLink.textContent = 'Download';
      downloadLink.className = 'download';

      if(clipName === null) {
        clipLabel.textContent = 'Untitled';
      } else {
        clipLabel.textContent = clipName;
      }

      clipContainer.appendChild(audio);
      clipContainer.appendChild(clipLabel);
      clipContainer.appendChild(deleteButton);
      clipContainer.appendChild(downloadLink);
      soundClips.appendChild(clipContainer);

      audio.controls = true;
      const blob = new Blob(chunks, { 'type' : 'audio/wav; codecs=opus' });
      chunks = [];
      const audioURL = window.URL.createObjectURL(blob);
      audio.src = audioURL;
      // createAudioElement(URL.createObjectURL(blob));
      console.log("recorder stopped");

      downloadLink.onclick = function(e) {
        var url = URL.createObjectURL(blob);
        var au = document.createElement('audio');
        var li = document.createElement('li');
        var link = document.createElement('a');
        //add controls to the <audio> element 
        au.controls = true;
        au.src = url;
        //link the a element to the blob 
        link.href = url;
        link.download = new Date().toISOString() + '.wav';
        link.innerHTML = link.download;
        //add the new audio and a elements to the li element 
        li.appendChild(au);
        li.appendChild(link);
        //add the li element to the ordered list 
        recordingsList.appendChild(li);
      }

      deleteButton.onclick = function(e) {
        let evtTgt = e.target;
        evtTgt.parentNode.parentNode.removeChild(evtTgt.parentNode);
      }

      clipLabel.onclick = function() {
        const existingName = clipLabel.textContent;
        const newClipName = prompt('Enter a new name for your sound clip?');
        if(newClipName === null) {
          clipLabel.textContent = existingName;
        } else {
          clipLabel.textContent = newClipName;
        }
      }
    }

    // function createDownloadLink() {
    //   recorder && recorder.exportWAV(function(blob) {
    //     var url = URL.createObjectURL(blob);
    //     var li = document.createElement('li');
    //     var au = document.createElement('audio');
    //     var hf = document.createElement('a');
        
    //     au.controls = true;
    //     au.src = url;
    //     hf.href = url;
    //     hf.download = new Date().toISOString() + '.wav';
    //     hf.innerHTML = hf.download;
    //     li.appendChild(au);
    //     li.appendChild(hf);
    //     recordingslist.appendChild(li);
    //   });
    // }

  //   function createAudioElement(blobUrl) {
  //     const downloadEl = document.createElement('a');
  //     downloadEl.style = 'display: block';
  //     downloadEl.innerHTML = 'download';
  //     downloadEl.download = 'audio.webm';
  //     downloadEl.href = blobUrl;
  //     const audioEl = document.createElement('audio');
  //     audioEl.controls = true;
  //     const sourceEl = document.createElement('source');
  //     sourceEl.src = blobUrl;
  //     sourceEl.type = 'audio/webm';
  //     audioEl.appendChild(sourceEl);
  //     document.body.appendChild(audioEl);
  //     document.body.appendChild(downloadEl);
  // }

  //   function createDownloadLink(blob) {
  //     var url = URL.createObjectURL(blob);
  //     var au = document.createElement('audio');
  //     var li = document.createElement('li');
  //     var link = document.createElement('a');
  //     //add controls to the <audio> element 
  //     au.controls = true;
  //     au.src = url;
  //     //link the a element to the blob 
  //     link.href = url;
  //     link.download = new Date().toISOString() + '.wav';
  //     link.innerHTML = link.download;
  //     //add the new audio and a elements to the li element 
  //     li.appendChild(au);
  //     li.appendChild(link);
  //     //add the li element to the ordered list 
  //     recordingsList.appendChild(li);
  // }

    mediaRecorder.ondataavailable = function(e) {
      chunks.push(e.data);
    }
  }

  let onError = function(err) {
    console.log('The following error occured: ' + err);
  }

  navigator.mediaDevices.getUserMedia(constraints).then(onSuccess, onError);

} else {
   console.log('getUserMedia not supported on your browser!');
}

function visualize(stream) {
  if(!audioCtx) {
    audioCtx = new AudioContext();
  }

  const source = audioCtx.createMediaStreamSource(stream);

  const analyser = audioCtx.createAnalyser();
  analyser.fftSize = 2048;
  const bufferLength = analyser.frequencyBinCount;
  const dataArray = new Uint8Array(bufferLength);

  source.connect(analyser);
  //analyser.connect(audioCtx.destination);

  draw()

  function draw() {
    const WIDTH = canvas.width
    const HEIGHT = canvas.height;

    requestAnimationFrame(draw);

    analyser.getByteTimeDomainData(dataArray);

    canvasCtx.fillStyle = 'rgb(200, 200, 200)';
    canvasCtx.fillRect(0, 0, WIDTH, HEIGHT);

    canvasCtx.lineWidth = 2;
    canvasCtx.strokeStyle = 'rgb(0, 0, 0)';

    canvasCtx.beginPath();

    let sliceWidth = WIDTH * 1.0 / bufferLength;
    let x = 0;


    for(let i = 0; i < bufferLength; i++) {

      let v = dataArray[i] / 128.0;
      let y = v * HEIGHT/2;

      if(i === 0) {
        canvasCtx.moveTo(x, y);
      } else {
        canvasCtx.lineTo(x, y);
      }

      x += sliceWidth;
    }

    canvasCtx.lineTo(canvas.width, canvas.height/2);
    canvasCtx.stroke();

  }
}

window.onresize = function() {
  canvas.width = mainSection.offsetWidth;
}

window.onresize();

// $(document).ready(function(){
//   $('.form_wrapper').on('click', '.upload', function(){
//      var data = $('.file').val();
//      $.ajax({
//       url: "/upload",
//      type: "get",
//      data: {text:data},
//      success: function(response) {
//        $(".results").html(response.predict);
//       }
//    });
//   });
// });

// $(document).ready(function() {
//   $('form').on('submit', function(event) {
//     $.ajax({
//        data : {
//           // Prediction : $('remove_wav').val(),
//           // YouTube: $('youtube_song_link').val(),
//           // Guitar : $('guitar_tab_song_link').val(),
//           FileName : $('filepath').val(),
//               },
//           type : 'POST',
//           url : '/upload'
//          })
//      .done(function(data) {
//        $('results').text(data.output).show();
//    });
//    event.preventDefault();
//    });
// });