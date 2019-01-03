import cv2
from PIL import ImageGrab
import numpy as np
import time

class Vision:
    def __init__(self):
        self.static_templates = {
            'level': 'assets/level.png',
            'I': 'assets/I.png',
            'J': 'assets/J.png',
            'L': 'assets/L.png',
            'O': 'assets/O.png',
            'S': 'assets/S.png',
            'T': 'assets/T.png',
            'Z': 'assets/Z.png',
            'nextI': 'assets/next/I.png',
            'nextJ': 'assets/next/J.png',
            'nextL': 'assets/next/L.png',
            'nextO': 'assets/next/O.png',
            'nextS': 'assets/next/S.png',
            'nextT': 'assets/next/T.png',
            'nextZ': 'assets/next/Z.png'
        }

        self.templates = { k: cv2.imread(v, 0) for (k, v) in self.static_templates.items() }

        self.width = 1400
        self.height = 1050

        self.frame = None

    def __take_screenshot(self, top, left, width, height):
        img = np.array(ImageGrab.grab(bbox=(top, left, width, height)))
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def get_image(self, path):
        return cv2.imread(path, 0)

    def refresh_frame(self):
        self.frame = self.__take_screenshot(280, 0, self.width, self.height)
    
    def display_frame(self):
        cv2.imshow('window', self.frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
        
    def match_template(self, img_grayscale, template, threshold=0.9):
        result = cv2.matchTemplate(img_grayscale, template, cv2.TM_CCOEFF_NORMED)
        matches = np.where(result >= threshold)
        return matches
    
    def find_template(self, name, image=None, threshold=0.9):
        if image is None:
            if self.frame is None:
                self.refresh_frame()

            image = self.frame

        return self.match_template(
            image,
            self.templates[name],
            threshold
        )
    
        

    def scaled_find_template(self, name, image=None, threshold=0.9, scales=[1.0, 0.9, 1.1]):
        if image is None:
            if self.frame is None:
                self.refresh_frame()

            image = self.frame

        initial_template = self.templates[name]
        for scale in scales:
            scaled_template = cv2.resize(initial_template, (0,0), fx=scale, fy=scale)
            matches = self.match_template(
                image,
                scaled_template,
                threshold
            )
            if np.shape(matches)[1] >= 1:
                return matches
        return matches