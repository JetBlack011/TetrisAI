# Scan code reference http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
import ctypes
import pyautogui
from time import sleep

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

class Controller:
    def __init__(self):
        # Key scan code constants
        self.SELECT = 0x36 # DIK_RSHIFT, Shift on main keyboard
        self.START  = 0x1C # DIK_RETURN, Enter on main keyboard
        self.UP     = 0x11 # DIK_W
        self.LEFT   = 0x1E # DIK_A
        self.RIGHT  = 0x20 # DIK_S
        self.DOWN   = 0x1F # DIK_D
        self.A      = 0x2C # DIK_PERIOD
        self.B      = 0x2D # DIK_COMMA

        self.KEY_RATE = 0.1

    ## Private actuals functions
    def __press_key(self, hexKeyCode):
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
        x = Input( ctypes.c_ulong(1), ii_ )
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    def __release_key(self, hexKeyCode):
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
        x = Input( ctypes.c_ulong(1), ii_ )
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    ## Simplified public controller API
    def press_start(self):
        self.__press_key(self.START)
        sleep(self.KEY_RATE)
        self.__release_key(self.START)

    def press_select(self):
        self.__press_key(self.SELECT)
        sleep(self.KEY_RATE)
        self.__release_key(self.SELECT)

    def press_up(self):
        self.__press_key(self.UP)
        sleep(self.KEY_RATE)
        self.__release_key(self.DOWN)

    def press_down(self):
        self.__press_key(self.DOWN)
        sleep(self.KEY_RATE)
        self.__release_key(self.DOWN)

    def hold_down(self):
        self.__press_key(self.DOWN)

    def release_down(self):
        self.__release_key(self.DOWN)

    def press_left(self):
        self.__press_key(self.LEFT)
        sleep(self.KEY_RATE)
        self.__release_key(self.LEFT)

    def press_right(self):
        self.__press_key(self.RIGHT)
        sleep(self.KEY_RATE)
        self.__release_key(self.RIGHT)

    def rotate_cw(self):
        self.__press_key(self.A)
        sleep(self.KEY_RATE)
        self.__release_key(self.A)

    def rotate_ccw(self):
        self.__press_key(self.B)
        sleep(self.KEY_RATE)
        self.__release_key(self.B)

    def click_screen(self):
        pyautogui.moveTo(70, 70)
        pyautogui.click()