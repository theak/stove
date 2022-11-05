import cv2, json

import common

def main():
	config = common.get_config()
	image = common.get_image(config)

	qr = cv2.QRCodeDetector()
	_, points = qr.detectMulti(image)

	min_max = common.get_min_max(points)

	config['min_max'] = min_max
	print("CONFIG: ", config)

	outstr = json.dumps(config, indent=2)

	if outstr:
		with open("config.json", "w") as f:
			f.write(outstr)
			f.close()

if __name__ == "__main__": main()