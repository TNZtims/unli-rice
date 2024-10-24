import pyautogui
import time

pyautogui.PAUSE = 0.2

def create_notepad_report(report_content):
  pyautogui.hotkey('win', 'r')
  pyautogui.write('notepad', interval=0.05)
  pyautogui.press('enter')
  time.sleep(1)
  pyautogui.hotkey('win', 'up')

  pyautogui.write(report_content, interval=0.1)
  pyautogui.hotkey('ctrl', 'a')
  time.sleep(1)
  pyautogui.press('backspace')
  time.sleep(1)
  pyautogui.hotkey('ctrl', 'w')
  time.sleep(1)
  pyautogui.hotkey('alt', 'tab')
  time.sleep(1)