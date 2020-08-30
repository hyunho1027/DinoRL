import numpy as np
import pyautogui as pag
import time
import os

class Env:
    def __init__(self):
        print("LET\'S START!")
        self.refresh = 10
        self.remember = None
        self.size = pag.screenshot().size
        self.target_size = (128,64)

        # Open Dino Game.
        os.system("start chrome")
        time.sleep(3)
        pag.typewrite("chrome://dino")
        pag.press("enter")

        # Full Screen mode
        pag.press('f11')
        time.sleep(1)

    def reset(self):
        is_start = False
        while not is_start:
            pag.press('up')
            is_start = not self.is_done()

        time.sleep(1)
        pag.press('up')

        screen = self.screenshot()
        state = np.dstack((screen, screen))
        self.remember = screen
        return state

    def step(self, action):
        key = 'up' if action == 1 else 'down'
        pag.press(key)

        screen = self.screenshot()
        state = np.dstack((self.remember, screen))
        self.remember = screen
        done = self.is_done()
        reward = -1 if done else 0.1
        return state, reward, done  

    def is_done(self):
        return pag.screenshot()==pag.screenshot()

    def screenshot(self):
        screen = pag.screenshot()
        screen = screen.convert('L')
        screen = screen.resize(self.target_size)
        screen = np.array(screen, dtype=float)
        screen = (255-screen)/255.
        return screen

    def close(self):
        pag.press('f11')
        pag.hotkey('ctrl', 'w')

