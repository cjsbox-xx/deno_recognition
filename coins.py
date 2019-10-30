from common_image_utils import *

coin_red_color_bounds = ColorBounds(lower_bounds = [75, 10, 94], upper_bounds = [100, 155, 232])
coin_gold_color_bounds = ColorBounds(lower_bounds = [19, 200, 200], upper_bounds = [100, 240, 240])

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
    predicate_values = [(OneCentPredicate(), 0.01), 
                        (TenCentsPredicate(), 0.1),
                        (OneEuroPredicate(), 1.0),
                        (TwoEurosPredicate(), 2.0)]
    def __init__(self, image):
        super().__init__(image)

    def provide(self):
        for predicate, value in self.predicate_values:
            if predicate.test(self.image):
                return value