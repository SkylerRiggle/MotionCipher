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

# TEMPORARY CODE FOR POINT EXTRACTION (USES RAW POSITIONS, NOT DIRECTIONS)

points: list[tuple[float, est.Landmark]] = [];

for idx in range(0, len(leftLabels)):
    if leftLabels[idx] == lab.EVENT_PRESS:
        points.append((
            controllerData.leftController[idx].timestamp,
            controllerData.leftController[idx].position
        ));

for idx in range(0, len(rightLabels)):
    if rightLabels[idx] == lab.EVENT_PRESS:
        points.append((
            controllerData.rightController[idx].timestamp,
            controllerData.rightController[idx].position
        ));

if len(points) == 0:
    print("No Presses Detected!");
    exit(0);
elif len(points) == 1:
    print("Only One Press Detected!");
    exit(0);

def byTime(value: tuple[float, est.Landmark]):
    return value[0];

points.sort(key=byTime);

import math;

print("(Angle, Distance, Time) Pairs:");
lastPoint = points[0];
for idx in range(1, len(points)):
    point = points[idx];

    print(
        str(idx) + ": (" +
            str(math.atan2(
                point[1].y - lastPoint[1].y,
                point[1].x - lastPoint[1].x
            )) + ", " +
            str(math.sqrt(
                pow(point[1].x - lastPoint[1].x, 2) +
                pow(point[1].y - lastPoint[1].y, 2)
            )) + ", " +
            str(point[0] - lastPoint[0]) +
        ")"
    );

    lastPoint = point;