import cv2
from PIL import ImageGrab
import numpy as np

class Vision:

    def __init__(self, show_window=False):
        self.static_templates = {
            'start': 'assets/start.png',
            'game_type': 'assets/game_type.png',
            'level': 'assets/name.png',
            'playing': 'assets/playing.png',
            'end': 'assets/end.png',
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

        self.templates = {k: cv2.imread(v, 0) for (k, v) in self.static_templates.items()}

        self.current_templates = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
        self.next_templates = ['nextI', 'nextJ', 'nextL', 'nextO', 'nextS', 'nextT', 'nextZ']

        self.show_window = show_window

        self.top = 280
        self.right = 0
        self.width = 1400
        self.height = 1050

        self.stats_top = 350
        self.stats_right = 300
        self.stats_width = 645
        self.stats_height = 900

        self.last_stats = None
        self.frame = None

    def __take_screenshot(self, top, left, width, height):
        img = np.array(ImageGrab.grab(bbox=(top, left, width, height)))
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def get_image(self, path):
        return cv2.imread(path, 0)

    def refresh_frame(self):
        self.frame = self.__take_screenshot(self.top, self.right, self.width, self.height)
    
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

    def can_see_object(self, template, threshold=0.9):
        matches = self.find_template(template, threshold=threshold)
        return np.shape(matches)[1] >= 1

    def update(self):
        self.refresh_frame()

        if self.show_window:
            self.display_frame()
    
    ## Game specific functions
    def current_piece(self):
        for template in self.current_templates:
            if self.can_see_object(template):
                return template
        return None
        
    def next_piece(self):
        for template in self.next_templates:
            if self.can_see_object(template):
                return (template[-1])
        return None

    def is_block_down(self):
        stats = self.__take_screenshot(self.stats_top,
                                       self.stats_right,
                                       self.stats_width,
                                       self.stats_height)
        return not np.array_equal(stats, self.last_stats)
    
    def update_stats(self):
        self.last_stats = self.__take_screenshot(self.stats_top,
                                                 self.stats_right,
                                                 self.stats_width,
                                                 self.stats_height)

    ## On Event functions
    def on_start(self):
        return self.can_see_object("start")
    
    def on_choose_game_type(self):
        return self.can_see_object("game_type")

    def on_choose_level(self):
        return self.can_see_object("level")

    def on_playing(self):
        return self.can_see_object("playing")
    
    def on_game_over(self):
        return self.can_see_object("end")