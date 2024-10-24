import pyautogui
import time
from .mouse_keyboard import smooth_scroll, simulate_mouse_movements

pyautogui.PAUSE = 0.2

def go_to_seller_central_pricing_health():
  pyautogui.hotkey('ctrl', 't')
  time.sleep(1)
  pyautogui.write('sellercentral.amazon.com/home', interval=0.15)
  pyautogui.press('enter')
  time.sleep(1)
  simulate_mouse_movements()
  pyautogui.moveTo(22, 143, duration=0.2)
  pyautogui.click()
  time.sleep(1)
  pyautogui.moveTo(127, 290, duration=0.2)
  pyautogui.moveTo(418, 297, duration=0.2)
  pyautogui.click()
  simulate_mouse_movements(2)
  pyautogui.moveTo(900, 500, duration=0.2)
  smooth_scroll(-5000, 2)
  pyautogui.moveTo(956, 905, duration=0.2)
  pyautogui.click()
  smooth_scroll(-7500, 2)
  simulate_mouse_movements(1)
  pyautogui.hotkey('ctrl', 'w')