import cv2, numpy

from hassapi import Hass

import common

def main():
    config = common.get_config()
    image = common.get_image(config)
    lower, upper = (numpy.array(config['lower']), numpy.array(config['upper']))
    min_max, max_area = (config['min_max'], config['max_area'])
    debug = config['debug']

    hass, hassurl, hasstoken, hassboolean = [None] * 4
    if 'hassurl' in config:
        hassurl, hasstoken, hassboolean = (config['hassurl'], config['hasstoken'], config['hassboolean'])
        hass = Hass(hassurl=hassurl, token=hasstoken)


    contours = get_contours(image, lower, upper, min_max, max_area)
    cnt = len(contours)
    if cnt > 0:
        print("stove is ON:", "%d contours" % cnt)
        if debug: cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
        if hass: hass.turn_on(hassboolean)
    else:
        print("stove is off")
        if hass: hass.turn_off(hassboolean)
    
    if debug:
        cv2.imshow("image", image)
        cv2.waitKey(0)

#Image, lower/upper BGR, ((min_x, min_y), (max_x, max_y)), max_area
def get_contours(image, lower, upper, min_max, max_area):
    mask = cv2.inRange(image, lower, upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return list(filter(common.range_filter(min_max, max_area), contours))

if __name__ == "__main__": main()