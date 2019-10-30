from common_image_utils import *

denomination_red_color_bounds = ColorBounds(lower_bounds = [65, 50, 150], upper_bounds = [80, 80, 160])
denomination_green_color_bounds = ColorBounds(lower_bounds = [65, 100, 70], upper_bounds = [80, 120, 80])
denomination_yellow_color_bounds = ColorBounds(lower_bounds = [100, 220, 230], upper_bounds = [130, 250, 255])
denomination_grey_color_bounds = ColorBounds(lower_bounds = [100, 100, 100], upper_bounds = [130, 130, 130])

class TenEurosPredicate(ImagePredicate):
    def test(self, image):
        colorRangeExtractor = ColorRangeImageExtractor(denomination_red_color_bounds)
        red_image = colorRangeExtractor.extract(image)
        ratio_to_black = get_ratio_to_black(red_image) * 10000
        return ratio_to_black >= 75 and ratio_to_black <= 90

class HundredEurosPredicate(ImagePredicate):
    def test(self, image):  
        colorRangeExtractor = ColorRangeImageExtractor(denomination_green_color_bounds)
        green_image = colorRangeExtractor.extract(image)
        ratio_to_black = get_ratio_to_black(green_image) * 10000
        return ratio_to_black >= 75 and ratio_to_black <= 90

class TwoHundredEurosPredicate(ImagePredicate):
    def test(self, image):
        colorRangeExtractor = ColorRangeImageExtractor(denomination_yellow_color_bounds)
        yellow_image = colorRangeExtractor.extract(image)
        ratio_to_black = get_ratio_to_black(yellow_image) * 10000
        return ratio_to_black >= 450 and ratio_to_black <= 500

class FiveEurosPredicate(ImagePredicate):
    def test(self, image):
        colorRangeExtractor = ColorRangeImageExtractor(denomination_grey_color_bounds)
        grey_image = colorRangeExtractor.extract(image)
        ratio_to_black = get_ratio_to_black(grey_image) * 10000
        return ratio_to_black >= 1100 and ratio_to_black <= 1150


class DenominationImageValueProvider(ImageValueProvider):
    predicate_values = [(TenEurosPredicate(), 10.0),
                        (HundredEurosPredicate(), 100.0),
                        (TwoHundredEurosPredicate(), 200.0),
                        (FiveEurosPredicate(), 5.0)]
    def __init__(self, image):
        super().__init__(image)

    def provide(self):
        for predicate, value in self.predicate_values:
            if predicate.test(self.image):
                return value