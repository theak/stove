import cv2, os, numpy

import common

DIR = "img/"
EXT = ".jpg"

def main():
    config = common.get_config()
    lower, upper = (numpy.array(config['lower']), numpy.array(config['upper']))
    min_max, max_area = (config['min_max'], config['max_area'])
    config["type"] = "file"
    for img in os.listdir(DIR):
        if not img.endswith(EXT): continue
        config["file"] = DIR + img
        image = common.get_image(config)
        contours = common.get_contours(image, lower, upper, min_max, max_area)
        success = len(contours) > 0 if img.startswith('on') else len(contours) == 0
        print(img, len(contours), success)

if __name__ == "__main__": main()