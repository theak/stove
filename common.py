import cv2, json, shutil

CONFIG = "config.json"
CONFIG_BAK = "config_bak.json"

def get_config():
    f = open(CONFIG)
    config = json.load(f)
    f.close()
    return config

def get_image(config):
    image = None
    if config['type'] == 'url':
        cap = cv2.VideoCapture(config['url'])
        _, image = cap.read()
    else:
        image = cv2.imread(config['file'])
    return image

def backup_config():
    shutil.copy(CONFIG, CONFIG_BAK)

def get_min_max(boxes):
    mins = [10000, 10000]
    maxes = [0, 0]
    for box in boxes:
        for coord in box:
            for i in range(0, 2):
                if coord[i] < mins[i]:
                    mins[i] = int(coord[i])
                if coord[i] > maxes[i]:
                    maxes[i] = int(coord[i])
    return (mins, maxes)

def range_filter(min_max, max_area):
    mins, maxes = min_max
    def out(c):
        x,y,w,h = cv2.boundingRect(c)
        return (x > mins[0] and x < maxes[0] and y > mins[1] and y < maxes[1]) and (w * h < max_area)
    return out

#Image, lower/upper BGR, ((min_x, min_y), (max_x, max_y)), max_area
def get_contours(image, lower, upper, min_max, max_area):
    mask = cv2.inRange(image, lower, upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return list(filter(range_filter(min_max, max_area), contours))

