from cv2 import Mat

class Frame:
    """
    A single frame of a video including both image and timing data.
    """
    image: Mat;
    timestamp: float;

    def __init__(self, image: Mat, timestamp: float):
        self.image = image;
        self.timestamp = timestamp;