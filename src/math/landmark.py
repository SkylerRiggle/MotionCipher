class Landmark:
    """
    Defines a landmark position in Euclidian space.
    """
    x: float;
    y: float;
    z: float;

    def __init__(self, x: float, y: float, z: float):
        self.x = x;
        self.y = y;
        self.z = z;