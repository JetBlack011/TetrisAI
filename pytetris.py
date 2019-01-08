import cv2
import time
import pyautogui as p
import numpy as np
from PIL import ImageGrab

def process_img(original_image):
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    return processed_img

last_time = time.time()

last = np.array([])

while True:
    screen = np.array(ImageGrab.grab(bbox=(350, 300, 645, 900)))
    new_screen = process_img(screen)

    print("loop took {} seconds".format(time.time() - last_time))
    print(np.array_equal(new_screen, last))
    last_time = time.time()

    cv2.imshow('window', new_screen)
    #cv2.imshow('window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
    
    last = new_screen