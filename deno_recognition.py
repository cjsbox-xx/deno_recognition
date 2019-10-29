import numpy as np
import cv2
import sys


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

coin_red_color_bounds = ColorBounds(lower_bounds = [75, 10, 94], upper_bounds = [100, 155, 232])
coin_gold_color_bounds = ColorBounds(lower_bounds = [19, 200, 200], upper_bounds = [100, 240, 240])
denomination_red_color_bounds = ColorBounds(lower_bounds = [65, 50, 150], upper_bounds = [80, 80, 160])
denomination_green_color_bounds = ColorBounds(lower_bounds = [65, 100, 70], upper_bounds = [80, 120, 80])
denomination_yellow_color_bounds = ColorBounds(lower_bounds = [100, 220, 230], upper_bounds = [130, 250, 255])
denomination_grey_color_bounds = ColorBounds(lower_bounds = [100, 100, 100], upper_bounds = [130, 130, 130])

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

class OneCentPredicate(ImagePredicate):
    def test(self, image):
        colorRangeExtractor = ColorRangeImageExtractor(coin_red_color_bounds)
        red_image = colorRangeExtractor.extract(image)
        red_value = UniqueColorCountValueProvider(red_image).provide()
        return red_value >= 200

class TenCentsPredicate(ImagePredicate):
    def test(self, image):
        colorRangeExtractor = ColorRangeImageExtractor(coin_gold_color_bounds)
        gold_image = colorRangeExtractor.extract(image)
        ratio_to_black = int(get_ratio_to_black(gold_image) * 10000)
        return ratio_to_black >= 1000 and ratio_to_black <= 1050

class OneEuroPredicate(ImagePredicate):
    def test(self, image):
        colorRangeExtractor = ColorRangeImageExtractor(coin_gold_color_bounds)
        gold_image = colorRangeExtractor.extract(image)
        ratio_to_black = int(get_ratio_to_black(gold_image) * 10000)
        return ratio_to_black == 498

class TwoEurosPredicate(ImagePredicate):
    def test(self, image): 
        colorRangeExtractor = ColorRangeImageExtractor(coin_gold_color_bounds)
        gold_image = colorRangeExtractor.extract(image)
        ratio_to_black = int(get_ratio_to_black(gold_image) * 10000)
        return ratio_to_black == 499

class CoinImageValueProvider(ImageValueProvider):
    def __init__(self, image):
        super().__init__(image)

    def provide(self):



class DenominationImageValueProvider(ImageValueProvider):
    def __init__(self, image):
        super().__init__(image)

    def provide(self):


def getColorRangedImage(image, lower_bounds, upper_bounds):
    lower = np.array(lower_bounds, dtype = "uint8")
    upper = np.array(upper_bounds, dtype = "uint8")
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask = mask)
    return output

def getRedImage(image):
    lower_red = [75, 10, 94]
    upper_red = [100, 155, 232]
    return getColorRangedImage(image, lower_red, upper_red)

def getGoldImage(image):
    lower_gold = [19, 200, 200]
    upper_gold = [100, 240, 240]
    return getColorRangedImage(image, lower_gold, upper_gold)

def unique_count_app(image):
    colors, count = np.unique(image.reshape(-1,image.shape[-1]), axis=0, return_counts=True)
    return colors[count.argmax() - 1]

def isRedImage(image):
    red_image = getRedImage(image)
    freq_color = unique_count_app(red_image)
    red_value = freq_color[2]
    return red_value >= 200

def isGoldImage(image):
    gold_image = getGoldImage(image)
    ratio_to_black = int(get_ratio_to_black(gold_image) * 10000)
    return ratio_to_black >= 1000 and ratio_to_black <= 1050

def isOneEuro(image):
    gold_image = getGoldImage(image)
    ratio_to_black = int(get_ratio_to_black(gold_image) * 10000)
    return ratio_to_black == 498

def isTwoEuro(image):
    gold_image = getGoldImage(image)
    ratio_to_black = int(get_ratio_to_black(gold_image) * 10000)
    return ratio_to_black == 499

def getCoinValue(image):
    if isRedImage(image):
        return 0.01
    if isGoldImage(image):
        return 0.1
    if isOneEuro(image):
        return 1.0
    if isTwoEuro(image):
        return 2.0
    return 10000.0

def getDenominationRedImage(image):
    lower_red = [65, 50, 150]
    upper_red = [80, 80, 160]
    return getColorRangedImage(image, lower_red, upper_red)

def getDenominationGreenImage(image):
    lower_green = [65, 100, 70]
    upper_green = [80, 120, 80]
    return getColorRangedImage(image, lower_green, upper_green)

def getDenominationYellowImage(image):
    lower_yellow = [100, 220, 230]
    upper_yellow = [130, 250, 255]
    return getColorRangedImage(image, lower_yellow, upper_yellow)

def getDenominationGrayImage(image):
    lower_gray = [100, 100, 100]
    upper_gray = [130, 130, 130]
    return getColorRangedImage(image, lower_gray, upper_gray)

def isDenominationRed(image):
    red_image = getDenominationRedImage(image)
    ratio_to_black = get_ratio_to_black(red_image) * 10000
    return ratio_to_black >= 75 and ratio_to_black <= 90

def isDenominationGreen(image):
    green_image = getDenominationGreenImage(image)
    ratio_to_black = get_ratio_to_black(green_image) * 10000
    return ratio_to_black >= 75 and ratio_to_black <= 90

def isDenominationYellow(image):
    yellow_image = getDenominationYellowImage(image)
    ratio_to_black = get_ratio_to_black(yellow_image) * 10000
    return ratio_to_black >= 450 and ratio_to_black <= 500

def isDenominationGray(image):
    grey_image = getDenominationGrayImage(image)
    ratio_to_black = get_ratio_to_black(grey_image) * 10000
    return ratio_to_black >= 1100 and ratio_to_black <= 1150

def getDenominationValue(image):
    if (isDenominationRed(image)):
        return 10.0
    if (isDenominationGreen(image)):
        return 100.0
    if (isDenominationYellow(image)):
        return 200.0
    if (isDenominationGray(image)):
        return 5.0
    return 10000.0

font = cv2.FONT_HERSHEY_COMPLEX
# Read image. 
image_path = sys.argv[1]
roi = cv2.imread(image_path)
orig_image = roi.copy()

change = 0.0
edged = cv2.Canny(roi, 30, 200) 
cv2.imshow('Detected thres ',edged)

contours,h = cv2.findContours(edged,  
    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
for cnt in contours:
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    if len(approx)==4:
        cv2.drawContours(roi,[cnt],0,(0,0,255),3)
        x,y,w,h = cv2.boundingRect(approx)
        rect = (x, y, w, h)
        print(rect)
        #cv2.rectangle(roi, (x, y), (x+w, y+h), (0, 0, 255), 1);
        cropped = orig_image[y: y + h, x: x + w]
        #cv2.imshow('Detected denomination',cropped)
        denomination_value = getDenominationValue(cropped)
        change = change + denomination_value
        cv2.putText(roi, str(denomination_value), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), lineType=cv2.LINE_AA) 
    elif len(approx) >= 12 and len(approx) <= 14:
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)
        x = int(x)
        y = int(y)
        radius = int(radius)
        cropped = orig_image[y - radius: y + radius, x - radius: x + radius]
        cv2.imshow('Detected coins',cropped)
        coin_value = getCoinValue(cropped)
        cv2.circle(roi,(x,y),radius,(0,0,255),2)
        cv2.putText(roi, str(coin_value), (x, y - radius), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), lineType=cv2.LINE_AA) 
        change = change + coin_value

cv2.imshow('Detected coins',roi)
print("Total denominations and coins sum: %.2f" % round(change, 2))
while(1):
    k = cv2.waitKey(33)
    if k==27:    # Esc key to stop
        break
    elif k==-1:  # normally -1 returned,so don't print it
        continue
    else:
        print(k) # else print its value
