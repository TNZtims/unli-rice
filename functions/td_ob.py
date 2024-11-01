from datetime import datetime, timedelta
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

image_path_1 = resource_path('images/not_working_final.png')
image_path_2 = resource_path('images/not_working_final_2.png')
image_path_3 = resource_path('images/start_working_again.png')
image_path_4 = resource_path('images/start_working_again_2.png')

def td_ob(mins, secs):
  while True:
    try:
      location1, location2 = None, None
      
      try:
        location1 = pyautogui.locateOnScreen(image_path_3, confidence=0.8)
      except pyautogui.ImageNotFoundException:
        pass

      try:
        location2 = pyautogui.locateOnScreen(image_path_4, confidence=0.8)
      except pyautogui.ImageNotFoundException:
        pass

      if location1 is not None or location2 is not None:
        break

    except Exception as e:
      print(f"Unexpected error: {e}")

    if pyautogui.position() == (0, 0):
      break

    time.sleep(1)

  interval = timedelta(minutes=max(0, int(mins)-3), seconds=int(secs))
  start_time = datetime.now()
  show_toast(f"Starting countdown {int(mins)-3} mins, {secs} secs", 3000, "top-right", "warning")

  secs = 0
  mins = 0
  while True:
    current_time = datetime.now()
    
    if current_time - start_time >= interval:
      break
    
    if pyautogui.position() == (0, 0):
      break
    time.sleep(1)
    secs+=1
    
    if secs == 60:
      secs = 0
      mins+=1
      show_toast(f"{mins+3} minutes...", 2000, "top-right", "info")
  
  while True:
    try:
      location3, location4 = None, None
      
      try:
        location3 = pyautogui.locateCenterOnScreen(image_path_3, confidence=0.8)
      except pyautogui.ImageNotFoundException:
        pass

      try:
        location4 = pyautogui.locateCenterOnScreen(image_path_4, confidence=0.8)
      except pyautogui.ImageNotFoundException:
        pass

      if location3 is not None or location4 is not None:
        show_toast("Start working again...", 3000, "top-right", "info")
        pyautogui.click(location3 or location4)
        time.sleep(1)
        pyautogui.hotkey('win', 'down')
        time.sleep(1)
        break

    except Exception as e:
      print(f"Unexpected error: {e}")

    if pyautogui.position() == (0, 0):
      break

    time.sleep(1)