from math import sqrt;
from src.math.landmark import Landmark;

def Magnitude(x: float, y: float, z: float):
    return sqrt((x*x) + (y*y) + (z*z));

class Transform:
    position: Landmark;
    forward: Landmark;
    timestamp: float;
    pullDistance: float;

    def __init__(
            self,
            timestamp: float,
            indexTip: Landmark,
            midTip: Landmark,
            handWrist: Landmark,
            bodyWrist: Landmark
        ):
        self.timestamp = timestamp;
        
        self.pullDistance = Magnitude(
            indexTip.x - handWrist.x,
            indexTip.y - handWrist.y,
            indexTip.z - handWrist.z
        );

        fX: float = midTip.x - handWrist.x;
        fY: float = midTip.y - handWrist.y;
        fZ: float = midTip.z - handWrist.z;
        fMag = Magnitude(fX, fY, fZ);
        self.forward = Landmark(fX / fMag, fY / fMag, fZ / fMag);

        self.position = Landmark(bodyWrist.x, bodyWrist.y, bodyWrist.z);

        