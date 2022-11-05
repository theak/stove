import cv2, os, numpy

from main import get_contours

import common

DIR = "img/"

lower = numpy.array([1, 1, 180])
upper = numpy.array([140, 140, 255])

def main():
    config = common.get_config()
    lower, upper = (numpy.array(config['lower']), numpy.array(config['upper']))
    min_max, max_area = (config['min_max'], config['max_area'])
    config["type"] = "file"
    for img in os.listdir(DIR):
        config["file"] = DIR + img
        image = common.get_image(config)
        contours = get_contours(image, lower, upper, min_max, max_area)
        success = len(contours) > 0 if img.startswith('on') else len(contours) == 0
        print(img, len(contours), success)

if __name__ == "__main__": main()