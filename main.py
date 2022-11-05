import cv2, numpy

from hassapi import Hass

import common

DEBUG = False
HASS = True


hass = Hass(hassurl="http://192.168.0.155:8123/", token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJiNDgxYzRiNzBlZTg0Nzc1ODZkYmFkOTA0ZDc0YTUzNyIsImlhdCI6MTY2NzE4NzgwMiwiZXhwIjoxOTgyNTQ3ODAyfQ.yUWsRTVJMS4wZmXAhTsHoKpcoTuuVM2n69j_qGSQT8k")

def main():
    config = common.get_config()
    image = common.get_image(config)
    lower, upper = (numpy.array(config['lower']), numpy.array(config['upper']))
    min_max, max_area = (config['min_max'], config['max_area'])

    contours = get_contours(image, lower, upper, min_max, max_area)
    cnt = len(contours)
    if cnt > 0:
        print("%d contours" % cnt)
        if DEBUG: cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
        print("STOVE IS ON")
        if HASS: hass.turn_on("input_boolean.kitchen_stove")
    else:
        print("stove is off")
        if HASS: hass.turn_off("input_boolean.kitchen_stove")

#Image, lower/upper BGR, ((min_x, min_y), (max_x, max_y)), max_area
def get_contours(image, lower, upper, min_max, max_area):
    mask = cv2.inRange(image, lower, upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return list(filter(common.range_filter(min_max, max_area), contours))

if __name__ == "__main__": main()