import cv2, time, sys

import common

DIR = "img/"
EXT = ".jpg"

def main():
	if len(sys.argv) < 2 or sys.argv[1] not in ('on', 'off', 'qr'):
		print("Argument needed. Usage: python3 save.py [on/off/qr]")
		return
	save(sys.argv[1])

def save(state):
	config = common.get_config()
	image = common.get_image(config)
	ts = int(time.time())

	filename = DIR + state + str(ts) + EXT
	cv2.imwrite(filename, image)

if __name__ == "__main__": main()
