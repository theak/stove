import cv2, numpy, time

from hassapi import Hass

import common

def detect(frame=0):
    config = common.get_config()
    image = common.get_image(config)
    lower, upper = (numpy.array(config['lower']), numpy.array(config['upper']))
    min_max, max_area = (config['min_max'], config['max_area'])
    debug, num_on_frames, num_off_frames, delay = config['debug'], config['num_on_frames'], config['num_off_frames'], config['delay']

    hass, hassurl, hasstoken, hassboolean, current_state = [None] * 5
    if 'hassurl' in config:
        hassurl, hasstoken, hassboolean = (config['hassurl'], config['hasstoken'], config['hassboolean'])
        hass = Hass(hassurl=hassurl, token=hasstoken)
        current_state = hass.get_state(hassboolean).state

    contours = common.get_contours(image, lower, upper, min_max, max_area)
    cnt = len(contours)
    if cnt > 0:
        if debug: cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
        if hass and current_state == "off": 
            if frame >= num_on_frames:
                print("TURNING ON")
                hass.turn_on(hassboolean)
            else:
                print("stove is ON:", "%d contours" % cnt)
                time.sleep(delay)
                detect(frame + 1) #Run again until num_frames to confirm change
    else:
        if hass and current_state == "on":
            if frame >= num_off_frames:
                print("TURNING OFF")
                print(hass.turn_off(hassboolean))
            else:
                print("stove is off")
                time.sleep(delay)
                detect(frame + 1)  #Run again until num_frames to confirm change
    
    if debug:
        cv2.imshow("image", image)
        cv2.waitKey(0)

if __name__ == "__main__": detect()