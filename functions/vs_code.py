import pyautogui
import time

pyautogui.PAUSE = 1 

def create_vs_code(code_content):
  pyautogui.press('win')
  time.sleep(2) 
  pyautogui.write('vscode', interval=0.3)
  pyautogui.press('enter')
  time.sleep(5) 
  # pyautogui.hotkey('win', 'up')
  pyautogui.hotkey('ctrl', 'alt', 'win', 'n')
  pyautogui.press('enter')

  lines = code_content.splitlines()

  for line in lines:
    pyautogui.write(line.strip(), interval=0.1)
    pyautogui.press('enter') 

  pyautogui.hotkey('ctrl', 'w')
  pyautogui.press('tab')
  pyautogui.press('enter')
  pyautogui.hotkey('alt', 'f4')
  
  time.sleep(5) 