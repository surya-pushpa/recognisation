# Recognisation

It's a Python application which helps to detect the recognised faces of a person, and it will further detect number of recognised appeared in a video or can use a utility tool for cctv footage to detect the faces.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the pre-requisites.

```bash
 pip install numpy
 pip install opencv-python
 pip install Pillow
 pip install Flask
 pip install requests 
```

## Usage

```python
In command line, run home.py file

=> python home.py

=> open http://localhost:5000/ in browser and start using.

=>Fill all the details of person,
 and for current, give the video file location manually.

 To record video, click on Start Capturing
 To stop and save video, click on Stop Capturing.
 To start detecting and training , click on Send, followed by 'Train' to start training the faces.

To begin with recognisation process, click on Start Recognising button at the bottom.

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
