from math import sqrt, pow;
from src.math.transform import Transform;

EVENT_NONE: int = 0;
EVENT_PRESS: int = 1;
EVENT_HELD: int = 2;
EVENT_RELEASE: int = 3;

def LabelTransforms(transforms: list[Transform]) -> list[int]:
    labels: list[int] = [];
    if len(transforms) == 0:
        return labels;

    avg: float = 0.0;
    for transform in transforms:
        avg += transform.pullDistance;
    avg /= len(transforms);

    stdDev: float = 0.0;
    for transform in transforms:
        stdDev += pow(transform.pullDistance - avg, 2);
    stdDev = avg - sqrt(stdDev / len(transforms));

    prevLabel: int = EVENT_NONE;
    for transform in transforms:
        belowDev: bool = transform.pullDistance < stdDev;
        curLabel: int;
        
        if prevLabel == EVENT_NONE or prevLabel == EVENT_RELEASE:
            curLabel = EVENT_PRESS if belowDev else EVENT_NONE;
        else:
            curLabel = EVENT_HELD if belowDev else EVENT_RELEASE;

        labels.append(curLabel);
        prevLabel = curLabel;

    return labels;