#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask,request,render_template,jsonify
from detect import detectFace
from multiprocessing import Process
from train import trainFaces
from recognise import recogniseFaces, getUsersAppeared


app = Flask(__name__)
labels = {}

@app.route('/home')
def root():
    return "Welcome to We Recognise You!";

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/trainingData', methods=['POST'])
def trainData():
    message = trainFaces();
    
    return jsonify({'message' : message})

@app.route('/getNamesList', methods=['GET'])
def getNames():
    return jsonify({'names' : labels})

@app.route('/usersAppeared', methods=['POST'])
def getKnownUsers():
    fileName = request.args['fileName']
    knownUsers = getUsersAppeared(labels, fileName)

    res = run_with_limited_time(getUsersAppeared,(labels, fileName), {}, 100)
    print(res)
    if res is False:
        message =  "Error in video, try uploading another video"
    else:
        message = "Video completed."
    
    return jsonify({'message' : message,
                    'knownUsers' : knownUsers})

@app.route('/startRecognising')
def redirect():
    return render_template('process.html')
    
@app.route('/recogniseData', methods=['POST'])
def startRecognising():
    global labels
    print(labels)
    fileName = request.args['fileName']
    if fileName is not None:
        res = run_with_limited_time(recogniseFaces,(labels, fileName), {}, 10)
        if res is False:
            message = "Error in video or time duration exceeds, try uploading another video"
        else:
            message = "Face Recognising completed."
    else:
        message = "Enter fileName"
    return jsonify({'message' : message})
#        try:
#            message = recogniseFaces(labels, fileName);
#        except:
#            message = "Error in video, try uploading another video"
#    timeDuration = getFileDuration(fileName)
#    print(timeDuration)
#    res = run_with_limited_time(recogniseFaces,(labels, fileName), {}, 100)
#    print(res)
#    if res is False:
#        message =  "Error in video, try uploading another video"
#    else:
#        message = "Video completed."

    

@app.route('/uploadVideoRecording', methods=['POST'])
def videoCapturing():
    userId = request.args['userId']
    userName = request.args['userName']
    fileName = request.args['fileName']
    global labels
    if userId is not None and userName is not None and fileName is not None:
        if userId in labels:
            message = "UserID already exists, try with different person and id"
            return
        
        labels[userId] = userName
        message = detect_face(userId, userName, fileName)
        
        return jsonify({
                'userId':userId,
                'userName':userName,
                'fileName':fileName,
                'error':message
                })
    
    return jsonify({'error' : 'Missing data!'})


def detect_face(userId, userName, fileName):
#    try:
#        detectFace(userId, userName, fileName);
#        return "Face Detection completed."
#    except :
#        return "Error in video or time duration exceeds, try uploading another video"
    res = run_with_limited_time(detectFace, (userId, userName, fileName), {}, 10)
    if res is False:
        return "Error in video or time duration exceeds, try uploading another video"
    else:
        return "Face Detection completed."
    
def run_with_limited_time(func, args, kwargs, time):
    """Runs a function with time limit

    :param func: The function to run
    :param args: The functions args, given as tuple
    :param kwargs: The functions keywords, given as dict
    :param time: The time limit in seconds
    :return: True if the function ended successfully. False if it was terminated.
    """
    p = Process(target=func, args=args, kwargs=kwargs)
    p.start()
    p.join(time)
    if p.is_alive():
        p.terminate()
        return False

    return True

if __name__ =='__main__':  
    app.run(debug = True)
    