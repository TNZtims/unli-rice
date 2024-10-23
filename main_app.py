import pyautogui
import pymsgbox
import time
import tkinter as tk
from tkinter import messagebox, Text
import cv2
import os
from datetime import datetime
import threading

pyautogui.PAUSE = 0.2

default_report = """
Accomplishment Report

Web Scraping Automation:
Successfully developed multiple web scraping scripts using Puppeteer and Cheerio for extracting detailed product information, including specifications, pricing, and images, from e-commerce websites like Sockwell, Footmates, and Old Friend Footwear.

Data Cleanup and Formatting:
Implemented efficient data extraction and cleanup processes, removing unnecessary newline characters and extra spaces, ensuring clean and structured data output.

Transition to Cheerio:
Converted Puppeteer-based scripts to Cheerio for faster scraping, improving performance in scraping product details and subheaders from web pages.

Browser Automation Enhancements:
Integrated the Stealth plugin with Puppeteer to handle automated browser interactions more reliably, including tasks such as logging in to websites and handling hidden elements.

API Integration & Middleware Improvements:
Enhanced the functionality of the makeApiRequest function in React components, improving error handling by adding navigation to the /login route on error conditions.
"""

report_content = default_report 
camera_running = threading.Event()

def open_camera_cv2():
  cap = cv2.VideoCapture(0)

  if not cap.isOpened():
    return

  image_saved = False 

  while camera_running.is_set(): 
    ret, frame = cap.read()
    if ret and not image_saved: 
      timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
      downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
      filename = os.path.join(downloads_path, f"unli_rice_{timestamp}.jpg")
      cv2.imwrite(filename, frame)
      image_saved = True  
    
    time.sleep(1)

  cap.release()
  cv2.destroyAllWindows()

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

def go_to_basecamp():
  pyautogui.hotkey('ctrl', 't')
  time.sleep(1)
  pyautogui.write('3.basecamp.com/3354094/projects', interval=0.15)
  pyautogui.press('enter')
  time.sleep(1)
  simulate_mouse_movements()
  pyautogui.moveTo(900, 500, duration=0.2)
  smooth_scroll(-1000, 1)
  pyautogui.moveTo(1245, 140, duration=0.2)
  pyautogui.click()
  time.sleep(1)
  pyautogui.moveTo(1342, 196, duration=0.2)
  pyautogui.click()
  pyautogui.write('rundown', interval=0.15)
  time.sleep(1)
  pyautogui.press('enter')
  pyautogui.moveTo(900, 500, duration=0.2)
  time.sleep(1)
  pyautogui.hotkey('ctrl', 'w')

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

def main():
  global report_content  
  root = tk.Tk()
  root.title("Unlimited Rice")
  root.geometry("500x350")
  root.resizable(False, True)

  font_style = ("Arial", 12)
  simulate_mouse = tk.BooleanVar()
  seller_central = tk.BooleanVar()
  basecamp = tk.BooleanVar()
  cycle_tabs = tk.BooleanVar()
  notepad_report = tk.BooleanVar()

  def show_report_input():
    report_window = tk.Toplevel(root)
    report_window.attributes("-fullscreen", True)
    report_window.title("Edit Report")
    report_text = Text(report_window, wrap='word')
    report_text.insert(tk.END, report_content) 
    report_text.pack(fill='both', expand=True)

    def save_report():
      global report_content 
      report_content = report_text.get("1.0", tk.END).strip() 
      report_window.destroy()

    tk.Button(report_window, text="Save", command=save_report, cursor="hand2", font=('Arial', 12), bg="green", fg="white").pack(padx=20, pady=25, fill='x')

  tk.Label(root, text="Menu Selection:", font=("Arial", 14)).pack(pady=5)

  tk.Checkbutton(root, text="Simulate Mouse Movements", variable=simulate_mouse, font=font_style, cursor="hand2").pack(anchor='w')
  tk.Checkbutton(root, text="Go to Seller Central Pricing Health", variable=seller_central, font=font_style, cursor="hand2").pack(anchor='w')
  tk.Label(root, text="* Ensure your Seller Central is logged in", font=("Arial", 8), fg="red").pack(anchor="w", pady=0, padx=30)
  tk.Checkbutton(root, text="Go to Basecamp", variable=basecamp, font=font_style, cursor="hand2").pack(anchor='w')
  tk.Label(root, text="* Ensure your Basecamp is logged in", font=("Arial", 8), fg="red").pack(anchor="w", pady=0, padx=30)
  tk.Checkbutton(root, text="Cycle Through Tabs", variable=cycle_tabs, font=font_style, cursor="hand2").pack(anchor='w')

  notepad_frame = tk.Frame(root)
  tk.Checkbutton(notepad_frame, text="Create Notepad Report", variable=notepad_report, font=font_style, cursor="hand2").pack(side="left", anchor='w')
  tk.Button(notepad_frame, text="Edit Report", command=show_report_input, font=font_style, cursor="hand2").pack(side="right", padx=10)
  notepad_frame.pack(anchor='w', pady=1)

  def execute_selected():
    result = pymsgbox.confirm(text='Run the selected tasks in a loop? Make sure that the next active tab is your browser', title='Confirm', buttons=['OK', 'Cancel'])
    if result == 'Cancel':
      return
    
    try:
      global camera_running 
      camera_running.set() 
      camera_thread = threading.Thread(target=open_camera_cv2, daemon=True)
      camera_thread.start()
      time.sleep(2)

      while camera_running.is_set(): 
        if simulate_mouse.get():
          simulate_mouse_movements()
        if seller_central.get():
          go_to_seller_central_pricing_health()
        if basecamp.get():
          go_to_basecamp()
        if cycle_tabs.get():
          cycle_through_tabs()
        if notepad_report.get():
          create_notepad_report(report_content)
    except Exception as e:
      pymsgbox.alert(text='Script successfully stopped', title='Alert', button='Ok')
      print(f"An error occurred: {e}")
    finally:
      camera_running.clear()

  tk.Button(root, text="Start", command=execute_selected, font=("Arial", 14, 'bold'), bg="green", fg="white", cursor="hand2").pack(pady=(50,0), padx=20, fill='x')
  tk.Label(root, text="Note: Move your cursor to top-left most part of your main screen to force stop", font=("Arial", 10, 'bold'), fg='red').pack(pady=(0,0))
  root.mainloop()

if __name__ == "__main__":
  main()