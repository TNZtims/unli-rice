import pyautogui
import time
from .mouse_keyboard import smooth_scroll, simulate_mouse_movements

pyautogui.PAUSE = 1

def go_to_basecamp():
  pyautogui.hotkey('ctrl', 't')
  pyautogui.write('3.basecamp.com/3354094/projects', interval=0.15)
  pyautogui.press('enter')
  simulate_mouse_movements()
  pyautogui.moveTo(900, 500, duration=0.2)
  smooth_scroll(-1000, 1)
  pyautogui.moveTo(1245, 140, duration=0.2)
  pyautogui.click()
  pyautogui.moveTo(1342, 196, duration=0.2)
  pyautogui.click()
  pyautogui.write('rundown', interval=0.15)
  time.sleep(3)
  pyautogui.moveTo(900, 500, duration=0.2)
  smooth_scroll(-1000, 1)
  pyautogui.press('enter')
  time.sleep(3)
  smooth_scroll(-1000, 1)
  pyautogui.hotkey('ctrl', 'w')
  time.sleep(3)