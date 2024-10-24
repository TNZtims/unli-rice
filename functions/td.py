import pyautogui
import time
import os
import sys

pyautogui.FAILSAFE = True

def resource_path(relative_path):
  if hasattr(sys, '_MEIPASS'):
    return os.path.join(sys._MEIPASS, relative_path)
  else:
    return os.path.join(os.path.abspath("."), relative_path)

image_path = resource_path('images/not_working_final.png')

def td():
  while True:
    try:
      location = pyautogui.locateOnScreen(image_path, confidence=0.5)  
      if location is not None:
        print("Image found!")
        break
    except pyautogui.ImageNotFoundException:
      print("Image not found.")
      
    if pyautogui.position() == (0, 0):
      print("Failsafe triggered")
      break

    time.sleep(1)

  pyautogui.press('esc')
  time.sleep(1)
  pyautogui.press('esc')
  time.sleep(1)
  pyautogui.hotkey('win', 'down')
  time.sleep(1)