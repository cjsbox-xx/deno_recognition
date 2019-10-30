import numpy as np
import cv2
from abc import ABCMeta, abstractmethod

def get_ratio_to_black(image):
    colors, count = np.unique(image.reshape(-1,image.shape[-1]), axis=0, return_counts=True)
    other_colors_sum = sum(count[1:])
    return other_colors_sum / count[0] 

class ColorBounds:
    def __init__(self, lower_bounds, upper_bounds):
        self.lower = lower_bounds
        self.upper = upper_bounds

class ImageExtractor:
    @abstractmethod
    def extract(self, image):
        pass

class ColorRangeImageExtractor:
    def __init__(self, color_bounds):
        self.color_bounds = color_bounds

    def extract(self, image):
        lower = np.array(self.color_bounds.lower, dtype = "uint8")
        upper = np.array(self.color_bounds.upper, dtype = "uint8")
        mask = cv2.inRange(image, lower, upper)
        output = cv2.bitwise_and(image, image, mask = mask)
        return output

class ValueProvider:
    @abstractmethod
    def provide(self):
        pass

class ImageValueProvider(ValueProvider):
    def __init__(self, image):
        self.image = image

class UniqueColorCountValueProvider(ImageValueProvider):
    def __init__(self, image):
        super().__init__(image)

    def provide(self):
        colors, count = np.unique(self.image.reshape(-1,self.image.shape[-1]), axis=0, return_counts=True)
        return colors[count.argmax() - 1][2] #don't know why it is here like that

class ImagePredicate:
    @abstractmethod
    def test(self, image):
        pass