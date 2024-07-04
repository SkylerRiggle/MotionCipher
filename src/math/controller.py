from src.math.transform import Transform;

class ControllerData:
    leftController: list[Transform];
    rightController: list[Transform];

    def __init__(self):
        self.leftController = [];
        self.rightController = [];