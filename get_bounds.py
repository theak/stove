import cv2, json

import common

def get_bounds():
	common.backup_config()
	config = common.get_config()
	image = common.get_image(config)

	qr = cv2.QRCodeDetector()
	_, points = qr.detectMulti(image)

	if type(points) == type(None):
		print("No QR code detected - returning")
		return None

	min_max = common.get_min_max(points)

	config['min_max'] = min_max
	print("CONFIG: ", config)

	outstr = json.dumps(config, indent=2)

	if outstr:
		with open("config.json", "w") as f:
			f.write(outstr)
			f.close()
			return True
	return None

if __name__ == "__main__": get_bounds()