import src.video.capture as cap;
from pyscript import document, display;

START_BUTTON = "#start-button";
STOP_BUTTON = "#stop-button";

isStreaming = False;

def CaptureLoop():
    frames: list[cap.Frame] = [];

    cap.OpenCamera(0);

    while isStreaming:
        hasFrame, frame = cap.CaptureFrame();

        if hasFrame:
            frames.append(frame);
    
        display(frame.image);

    cap.CloseCamera();

def StartCapture():
    if isStreaming:
        return;

    isStreaming = True;
    document.querySelector(START_BUTTON).hidden = True;
    document.querySelector(STOP_BUTTON).hidden = False;

    CaptureLoop();

def EndCapture():
    if not isStreaming:
        return;

    isStreaming = False;
    document.querySelector(START_BUTTON).hidden = False;
    document.querySelector(STOP_BUTTON).hidden = True;