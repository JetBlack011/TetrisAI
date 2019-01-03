import cv2
import time
import pyautogui as p
import numpy as np
from PIL import ImageGrab

def process_img(original_image):
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    return processed_img

last_time = time.time()

while True:
    screen = np.array(ImageGrab.grab(bbox=(280, 0, 1400, 1050)))
    new_screen = process_img(screen)

    print("loop took {} seconds".format(time.time() - last_time))
    last_time = time.time()

    cv2.imshow('window', new_screen)
    #cv2.imshow('window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break