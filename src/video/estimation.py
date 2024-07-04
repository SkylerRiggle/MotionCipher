import cv2 as cv;
import mediapipe as mp;
from src.video.frame import Frame;
from src.math.landmark import Landmark;
from src.math.transform import Transform;
from src.math.controller import ControllerData;

MP_DRAW = mp.solutions.drawing_utils;
MP_HANDS = mp.solutions.hands;
MP_POSE = mp.solutions.pose;

LEFT_LABEL: str = "Left";

H_IDX_TIP: int = 8;
H_MID_TIP: int = 9;
H_WRIST: int = 0;
B_L_WRIST: int = 15;
B_R_WRIST: int = 16;

def EstimateLandmarks(frames: list[Frame]) -> tuple[list[Frame], ControllerData]:
    """
    Performs landmark estimations for the hands and body of a presumed single user in a video.
    """
    data: ControllerData = ControllerData();
    drawFrames: list[Frame] = [];

    hands = MP_HANDS.Hands();
    body = MP_POSE.Pose();

    for frame in frames:
        procImage = cv.cvtColor(frame.image, cv.COLOR_BGR2RGB);
    
        bodyData = body.process(procImage);
        if bodyData.pose_world_landmarks == None:
            continue;

        handData = hands.process(procImage);
        if handData.multi_hand_world_landmarks == None:
            continue;
    
        drawImage = frame.image.copy();
        bodyLandmarks = bodyData.pose_world_landmarks;
        handLandmarks = handData.multi_hand_world_landmarks;

        # Draw the body landmark data
        MP_DRAW.draw_landmarks(
            drawImage,
            bodyData.pose_landmarks,
            MP_POSE.POSE_CONNECTIONS
        );
    
        for idx in range(0, len(handLandmarks)):
            isLeft: bool = handData.multi_handedness[idx].classification[0].label == LEFT_LABEL;
        
            # Draw the hand landmark data
            MP_DRAW.draw_landmarks(
                drawImage,
                handData.multi_hand_landmarks[idx],
                MP_HANDS.HAND_CONNECTIONS
            );
            
            controllerTransform: Transform = Transform(
                frame.timestamp,
                Landmark(
                    handLandmarks[idx].landmark[H_IDX_TIP].x,
                    handLandmarks[idx].landmark[H_IDX_TIP].y,
                    handLandmarks[idx].landmark[H_IDX_TIP].z
                ),
                Landmark(
                    handLandmarks[idx].landmark[H_MID_TIP].x,
                    handLandmarks[idx].landmark[H_MID_TIP].y,
                    handLandmarks[idx].landmark[H_MID_TIP].z
                ),
                Landmark(
                    handLandmarks[idx].landmark[H_WRIST].x,
                    handLandmarks[idx].landmark[H_WRIST].y,
                    handLandmarks[idx].landmark[H_WRIST].z
                ),
                Landmark(
                    bodyLandmarks.landmark[B_L_WRIST if isLeft else B_R_WRIST].x,
                    bodyLandmarks.landmark[B_L_WRIST if isLeft else B_R_WRIST].y,
                    bodyLandmarks.landmark[B_L_WRIST if isLeft else B_R_WRIST].z
                )
            );
        
            if isLeft:
                data.leftController.append(controllerTransform);
            else:
                data.rightController.append(controllerTransform);

        drawFrames.append(Frame(drawImage, frame.timestamp));

    return drawFrames, data;