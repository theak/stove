'''
Script to configure Android IP cameras over http
Update ZOOM, CROP_X, and CROP_Y to be the right values for your setup
'''
URL = "http://192.168.0.101:8080"
ZOOM = 100
CROP_X = 64 #/settings/crop_x?set=41
CROP_Y = 52
CROP_URL = "/settings/crop_%s?set=%d"

import requests

def configure():
	status_code = requests.get(URL + "/ptz?zoom=%d" % ZOOM).status_code
	if status_code == 200:
		requests.get(URL + CROP_URL % ('x', CROP_X))
		requests.get(URL + CROP_URL % ('y', CROP_Y))
	return status_code

if __name__ == "__main__": print(configure())