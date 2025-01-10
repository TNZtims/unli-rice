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

start_working_image_path_100 = resource_path('images/start_working_again.png')
start_working_image_path_150 = resource_path('images/start_working_again_2.png')
start_working_image_path_125 = resource_path('images/start_working_again_3.png')

def td_ob(hours, mins, secs):
  print(f'Hours: {hours}, Minutes: {mins}, Seconds: {secs}')
  while True:
    try:
      location1A, location2A, location3A = None, None, None
      
      try:
        location1A = pyautogui.locateOnScreen(start_working_image_path_100, confidence=0.8)
      except pyautogui.ImageNotFoundException:
        pass

      try:
        location2A = pyautogui.locateOnScreen(start_working_image_path_150, confidence=0.8)
      except pyautogui.ImageNotFoundException:
        pass
      
      try:
        location3A = pyautogui.locateOnScreen(start_working_image_path_125, confidence=0.8)
      except pyautogui.ImageNotFoundException:
        pass

      if location1A is not None or location2A is not None or location3A is not None:
        break

    except Exception as e:
      print(f"Unexpected error: {e}")

    if pyautogui.position() == (0, 0):
      break

    time.sleep(1)

  interval = timedelta(hours=int(hours), minutes=int(mins), seconds=int(secs)) - timedelta(minutes=3)
  start_time = datetime.now()
  show_toast(f"Starting countdown {hours} hours, {mins} minutes, {secs} seconds (3 minutes subtracted)", 3000, "top-right", "warning")

  elapsed_secs = 0
  elapsed_mins = 0
  elapsed_hours = 0

  while True:
    current_time = datetime.now()
    
    if current_time - start_time >= interval:
      break
    
    if pyautogui.position() == (0, 0):
      break
    time.sleep(1)
    elapsed_secs += 1
    
    if elapsed_secs == 60:
      elapsed_secs = 0
      elapsed_mins += 1
      if elapsed_mins % 60 == 0:
        elapsed_mins = 0
        elapsed_hours += 1
      show_toast(f"{elapsed_hours} hours, {elapsed_mins + 3} minutes elapsed...", 2000, "top-right", "info")

  while True:
    try:
      location1B, location2B, location3B = None, None, None
      
      try:
        location1B = pyautogui.locateCenterOnScreen(start_working_image_path_100, confidence=0.8)
      except pyautogui.ImageNotFoundException:
        pass

      try:
        location2B = pyautogui.locateCenterOnScreen(start_working_image_path_150, confidence=0.8)
      except pyautogui.ImageNotFoundException:
        pass
      
      try:
        location3B = pyautogui.locateCenterOnScreen(start_working_image_path_125, confidence=0.8)
      except pyautogui.ImageNotFoundException:
        pass

      if location1B is not None or location2B is not None or location3B is not None:
        show_toast("Start working again...", 3000, "top-right", "info")
        pyautogui.click(location1B or location2B or location3B)
        time.sleep(1)
        pyautogui.hotkey('win', 'down')
        time.sleep(1)
        break

    except Exception as e:
      print(f"Unexpected error: {e}")

    if pyautogui.position() == (0, 0):
      break

    time.sleep(1)