var CandidateVideoCapturing = {};
var recordedBlobs = [];
var candidateVideoMediaStream;

function startVideoCapturing() {
    CandidateVideoCapturing.init();
}

function stopVideoCapturing() {
    CandidateVideoCapturing.stopVideoRecording(candidateVideoMediaRecorder);
}

function trainData() {
    $.ajax({
        url: '/trainingData',
        // data: blob,
        type: 'POST',
        // processData: false,
        // contentType: false,
        success: function(response) {
            console.log(response);
            window.alert(response.message);
        },
        error: function(error) {
            console.log(error);

        }
    });
}

function getListOfNames(){
    console.log("****");
    var newData;
    $.ajax({
        url: '/getNamesList',
        // data: blob,
        type: 'GET',
        processData: false,
        contentType: false,
        success: function(response) {
            console.log(response);
            newData = JSON.stringify(response.names);
            document.getElementById("namesList").innerHTML = newData;
        },
        error: function(error) {
            console.log(error);

        }
    });
}

function getUsersAppeared(){
    var usersAppeared;
    var fileName = document.getElementById("fileName2").value;
    $.ajax({
        url: '/usersAppeared?fileName=' + fileName,
        // data: blob,
        type: 'POST',
        processData: false,
        contentType: false,
        success: function(response) {
            console.log(response);
            newData = JSON.stringify(response.names);
            document.getElementById("usersAppeared").innerHTML = usersAppeared;
        },
        error: function(error) {
            console.log(error);

        }
    });
}

function startVideoRecognising(fileName) {
    var fileName = document.getElementById("fileName2").value;
    $.ajax({
        url: '/recogniseData?fileName=' + fileName,
        // data: blob,
        type: 'POST',
        processData: false,
        contentType: false,
        success: function(response) {
            console.log(response);
            window.alert(response.message);
        },
        error: function(error) {
            console.log(error);

        }
    });
}

function uploadRecording() {
    console.log("**upload started***");
    var userId = document.getElementById("userId").value;
    var userName = document.getElementById("userName").value;
    var fileName = document.getElementById("fileName").value;

    var targetUrl = window.location.href + "uploadVideoRecording?userId=" + userId + "&userName=" + userName + "&fileName=" + fileName;
    var paramName = "candidateVideo";
    CandidateVideoCapturing.uploadCandidateVideo(recordedBlobs, targetUrl, paramName);
}

CandidateVideoCapturing.init = function() {
    console.log("***\n\n***");
    CandidateVideoCapturing.requestCamera();

}

CandidateVideoCapturing.requestCamera = function() {
    navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;

    if (navigator.getUserMedia) {
        navigator.getUserMedia(
            window.constraints = {
                audio: {
                    echoCancellation: { exact: true }
                },
                video: true
            },
            function(stream) {
                console.log("got local media stream");
                var video = document.querySelector('#CandidateVC');
                video.srcObject = stream;
                video.muted = "muted";
                var candidateVideoMediaStream = stream;

                try {
                    candidateVideoMediaRecorder = new MediaRecorder(candidateVideoMediaStream, {
                        mimeType: 'video/webm;codecs=vp9',
                        // audioBitsPerSecond: 128000,
                        videoBitsPerSecond: 256000
                    });

                    CandidateVideoCapturing.startVideoRecording(candidateVideoMediaRecorder, 100);
                    CandidateVideoCapturing.handleVideoRecording(candidateVideoMediaRecorder);


                } catch (e) {
                    console.error('Exception while creating MediaRecorder:', e);
                    return;
                }
            },
            function(err) {
                console.log("Error occurred: " + err.name);
            }
        );
    } else {
        console.log("getUserMedia not supported");
    }
};
CandidateVideoCapturing.handleVideoRecording = function(recorder) {

    console.log('\nRecorded Blobs: ', recordedBlobs, candidateVideoMediaRecorder);
    recorder.ondataavailable = function(event) {
        if (event.data && event.data.size > 0) {
            recordedBlobs.push(event.data);
        }
    }
}
CandidateVideoCapturing.startVideoRecording = function(recorder, timeSlice) {
    console.log("Recording started");
    recordedBlobs = [];
    recorder.start(timeSlice);
};
CandidateVideoCapturing.stopVideoRecording = function(recorder) {
    console.log("Recording stopped");
    recorder.stream.getTracks().forEach(track => track.stop())
    CandidateVideoCapturing.downloadCandidateVideo(recordedBlobs, "avai");
};

CandidateVideoCapturing.downloadCandidateVideo = function(rB, name) {
    console.log(rB);
    var blob = new Blob(rB, {
        type: 'video/webm'
    });
    console.log(blob, blob.size);
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = name + '.webm';
    a.target = "_blank";
    document.body.appendChild(a);
    a.click();

    setTimeout(function() {
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }, 100);
}

CandidateVideoCapturing.uploadCandidateVideo = function(rB, targetUrl, paramName) {
    // console.log(rB);
    // var video_fmt = 'webm';
    // var blob = new Blob(rB, {
    //     type: 'video/' + video_fmt
    // });

    $.ajax({
        url: targetUrl,
        // data: blob,
        type: 'POST',
        processData: false,
        contentType: false,
        success: function(response) {
            console.log(response, response.error);
            window.alert(response.error);


        },
        error: function(error) {
            console.log(error);

        }
    });


    // // contruct use AJAX object
    // var http = new XMLHttpRequest();
    // http.open("POST", targetUrl, true);
    // // http.withCredentials = "true"

    // // stuff into a form, so servers can easily receive it as a standard file
    // // upload
    // var form = new FormData();
    // form.append(paramName, blob, paramName + "." + video_fmt);
    // console.log(form, blob);
    // // send data to server
    // http.send(form);

}