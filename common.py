import cv2, json

def get_config():
    f = open("config.json")
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

