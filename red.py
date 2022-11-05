import cv2, math, numpy, time

from hassapi import Hass

INFINITY = 10000
NFRAME = 2
TARGET_BRIGHTNESS = 100

cap = cv2.VideoCapture("http://192.168.0.101:8080/video")
hass = Hass(hassurl="http://192.168.0.155:8123/", token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJiNDgxYzRiNzBlZTg0Nzc1ODZkYmFkOTA0ZDc0YTUzNyIsImlhdCI6MTY2NzE4NzgwMiwiZXhwIjoxOTgyNTQ3ODAyfQ.yUWsRTVJMS4wZmXAhTsHoKpcoTuuVM2n69j_qGSQT8k")

def main():
    count = 0
    lower = numpy.array([1, 1, 180])
    upper = numpy.array([140, 140, 255])
    qr = cv2.QRCodeDetector()
    if True:
        #_, image = cap.read()
        image = cv2.imread("stoveon.jpg",)
        #if type(image) == type(None): continue
        norm = numpy.zeros((800,800))
        #image = cv2.normalize(image,  norm, 0, 255, cv2.NORM_MINMAX)
        _, points = qr.detectMulti(image)
        print("POINTS", points)
        min_max = get_min_max(points)
        #image = image[200:400, 300:600] #crop for 800 x 600
        if (count % NFRAME == 0):
            #brightness = image.mean()
            #print(brightness)
            imghsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            cv2.imshow("test", image)
            
            count = 0
            mask = cv2.inRange(image, lower, upper)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            contours = filter(range_filter(min_max), contours)
            cnt = len(list(filter(small, contours)))
            if cnt > 0:
                print("%d contours" % cnt)
                #cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
                print("STOVE IS ON")
                hass.turn_on("input_boolean.kitchen_stove")
            else:
                print("stove is off")
                hass.turn_off("input_boolean.kitchen_stove")
            
            #cv2.waitKey(0)
        #else: time.sleep(1)
        count += 1

    cap.release()
    cv2.destroyAllWindows()

MAX_SIZE = 100

def get_min_max(boxes):
    mins = [10000, 10000]
    maxes = [0, 0]
    for box in boxes:
        for coord in box:
            for i in range(0, 2):
                if coord[i] < mins[i]:
                    mins[i] = coord[i]
                if coord[i] > maxes[i]:
                    maxes[i] = coord[i]
    return (mins, maxes)

def range_filter(min_max):
    mins, maxes = min_max
    def out(c):
        x,y,w,h = cv2.boundingRect(c)
        print("x, y, w, h: ", x, y, w, h)
        return (x > mins[0] and x < maxes[0] and y > mins[1] and y < maxes[1])
    return out

def small(c):
    area = cv2.contourArea(c)
    print("area: ", area)
    return area < 5

if __name__ == "__main__":
    main()

''' points:
    array([[[261.     , 191.     ],
            [596.9967 , 191.     ],
            [598.1059 , 528.1835 ],
            [261.     , 526.99646]]], dtype=float32)'''
