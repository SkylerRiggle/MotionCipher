import cv2 as cv;
import src.event.labels as lab;
import src.video.capture as cap;
import src.video.estimation as est;
from src.video.frame import Frame;

OUTPUT_WINDOW: str = "MotionCipher";
ESC_KEY: int = 27;

cap.OpenCamera(0);
cv.namedWindow(OUTPUT_WINDOW);

frames: list[Frame] = [];
while (
        cv.waitKey(1) != ESC_KEY and
        cv.getWindowProperty(OUTPUT_WINDOW, cv.WND_PROP_VISIBLE) != 0
    ):
    hasFrame, frame = cap.CaptureFrame();

    if not hasFrame:
        continue;

    cv.imshow(OUTPUT_WINDOW, frame.image);
    frames.append(frame);

cv.destroyAllWindows();
cap.CloseCamera();

frames, controllerData = est.EstimateLandmarks(frames);
leftLabels = lab.LabelTransforms(controllerData.leftController);
rightLabels = lab.LabelTransforms(controllerData.rightController);
