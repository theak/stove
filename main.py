import cv2, numpy, time

from hassapi import Hass

import common

def main(frame=0):
    config = common.get_config()
    image = common.get_image(config)
    lower, upper = (numpy.array(config['lower']), numpy.array(config['upper']))
    min_max, max_area = (config['min_max'], config['max_area'])
    debug, num_frames, delay = config['debug'], config["num_frames"], config["delay"]

    hass, hassurl, hasstoken, hassboolean, current_state = [None] * 5
    if 'hassurl' in config:
        hassurl, hasstoken, hassboolean = (config['hassurl'], config['hasstoken'], config['hassboolean'])
        hass = Hass(hassurl=hassurl, token=hasstoken)
        current_state = hass.get_state(hassboolean).state

    contours = common.get_contours(image, lower, upper, min_max, max_area)
    cnt = len(contours)
    if cnt > 0:
        print("stove is ON:", "%d contours" % cnt)
        if debug: cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
        if hass and current_state == "off": 
            if frame >= num_frames: 
                print("TURNING ON")
                hass.turn_on(hassboolean)
            else:
                time.sleep(delay)
                main(frame + 1) #Run again until num_frames to confirm change
    else:
        print("stove is off")
        if hass and current_state == "on":
            if frame >= num_frames:
                print("TURNING OFF")
                print(hass.turn_off(hassboolean))
            else:
                time.sleep(delay)
                main(frame + 1)  #Run again until num_frames to confirm change
    
    if debug:
        cv2.imshow("image", image)
        cv2.waitKey(0)

if __name__ == "__main__": main()