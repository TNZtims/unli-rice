import pyautogui
import time
import os
import sys
from utils.toast import show_toast

pyautogui.FAILSAFE = True

def resource_path(relative_path):
  if hasattr(sys, '_MEIPASS'):
    return os.path.join(sys._MEIPASS, relative_path)
  else:
    return os.path.join(os.path.abspath("."), relative_path)

not_working_image_path_100 = resource_path('images/not_working_final.png')
not_working_image_path_150 = resource_path('images/not_working_final_2.png')
not_working_image_path_125 = resource_path('images/not_working_final_3.png')

def td():
  show_toast("Auto Yes Bypass enabled!", 2000, "top-right", "warning")
  
  while True:
    try:
      location1, location2, location3 = None, None, None
      
      try:
        location1 = pyautogui.locateOnScreen(not_working_image_path_100, confidence=0.5)
      except pyautogui.ImageNotFoundException:
        pass

      try:
        location2 = pyautogui.locateOnScreen(not_working_image_path_150, confidence=0.5)
      except pyautogui.ImageNotFoundException:
        pass
      
      try:
        location3 = pyautogui.locateOnScreen(not_working_image_path_125, confidence=0.5)
      except pyautogui.ImageNotFoundException:
        pass

      if location1 is not None or location2 is not None or location3 is not None:
        break

    except Exception as e:
      print(f"Unexpected error: {e}")

    if pyautogui.position() == (0, 0):
      break

    time.sleep(1)

  show_toast("I got you!", 2000, "top-right", "info")
  pyautogui.press('esc')
  time.sleep(1)
  pyautogui.press('esc')
  time.sleep(1)
  pyautogui.hotkey('win', 'down')
  time.sleep(1)