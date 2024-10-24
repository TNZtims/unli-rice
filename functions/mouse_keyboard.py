import pyautogui
import time

pyautogui.PAUSE = 0.2

def simulate_mouse_movements(repeat=3):
  for _ in range(repeat):
    pyautogui.moveTo(400, 400, duration=0.15)
    pyautogui.moveTo(400, 800, duration=0.15)
    pyautogui.moveTo(1200, 800, duration=0.15)
    pyautogui.moveTo(1200, 400, duration=0.15)

def smooth_scroll(scroll_amount, duration):
  steps = 100
  scroll_per_step = scroll_amount // steps
  time_per_step = duration / steps
  for _ in range(steps):
    pyautogui.scroll(scroll_per_step)
    time.sleep(time_per_step)
    
def cycle_through_tabs(repeat=10):
  for _ in range(repeat):
    pyautogui.hotkey('ctrl', 'tab')
    time.sleep(1)