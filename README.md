## Denomination and coins recognition

Example of using Python 3 to process images.

Example of usage:

```
python deno_recognition.py simple_01.bmp
```

In `common_image_utils.py` you will find base classes and some utils for processing images.
In `coins.py` and in `denominations.py` you will find concrete implementations for recognition coins and denominations values.

Algorythm is simple:

* Transform image to "edgie" with `cv2.Canny` method
* Find contours on that "edie" image with `cv2.findContours`
* Iterate over found contours
* If the contour is rectangle then consider it is a paper denomination and recognize it via `DenominationImageValueProvider`
* If the contour is circle then consider it is a coin and recognize value via `CoinImageValueProvider`
* Recognition is very simple and based on "amount" of color in the cropped contour or on ratio to black color. Very simple level of recognition

Welcome:)
