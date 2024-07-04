import cv2 as cv;
from time import time;
from src.video.frame import Frame;

########################################
############# File Capture #############
########################################

def ParseVideo() -> list[Frame]:
    """
    Parses the provided video file into a list of frames.
    """
    frames: list[Frame] = [];

    # TODO

    return frames;

########################################
########### Realtime Capture ###########
########################################
camera: cv.VideoCapture = cv.VideoCapture();

def OpenCamera(camIdx: int):
    """
    Opens an OpenCV video capture using the specified camera index.
    """
    if not camera.isOpened():
        camera.open(camIdx);

def CaptureFrame() -> tuple[bool, Frame]:
    """
    Captures a single video frame from the currently open camera.
    If no camera is open or if no image data is available, this method returns (False, None).
    """
    if not camera.isOpened():
        return False, None;

    hasData, image = camera.read();

    if not hasData:
        return False, None;
    
    return True, Frame(
        cv.flip(image, 1),
        time()
    );

def CloseCamera():
    """
    Closes the currently opened OpenCV camera.
    """
    if camera.isOpened():
        camera.release();