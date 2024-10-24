import cv2
import os
import pyautogui
import pymsgbox
import threading
import time
import tkinter as tk
from datetime import datetime
from functions.mouse_keyboard import simulate_mouse_movements, cycle_through_tabs
from functions.seller_central import go_to_seller_central_pricing_health
from functions.basecamp import go_to_basecamp
from functions.notepad import create_notepad_report
from functions.vs_code import create_vs_code
from functions.td import td
from tkinter import Text
from utils.initial_values import default_report, default_code

pyautogui.PAUSE = 0.2

report_content = default_report 
code_content = default_code
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

def main():
  global report_content, code_content  
  root = tk.Tk()
  root.title("Unlimited Rice")
  root.geometry("500x400")
  root.resizable(False, True)

  font_style = ("Arial", 12)
  simulate_mouse = tk.BooleanVar()
  seller_central = tk.BooleanVar()
  basecamp = tk.BooleanVar()
  cycle_tabs = tk.BooleanVar()
  notepad_report = tk.BooleanVar()
  vs_code = tk.BooleanVar()
  td_nw = tk.BooleanVar()

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

  def show_vs_code_input():
    vs_code_window = tk.Toplevel(root)
    vs_code_window.attributes("-fullscreen", True)
    vs_code_window.title("Edit Report")
    vs_code_text = Text(vs_code_window, wrap='word')
    vs_code_text.insert(tk.END, code_content) 
    vs_code_text.pack(fill='both', expand=True)

    def save_vs_code():
      global code_content 
      code_content = vs_code_text.get("1.0", tk.END).strip() 
      vs_code_window.destroy()

    tk.Button(vs_code_window, text="Save", command=save_vs_code, cursor="hand2", font=('Arial', 12), bg="green", fg="white").pack(padx=20, pady=25, fill='x')

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

  vs_code_frame = tk.Frame(root)
  tk.Checkbutton(vs_code_frame, text="Code Javascript in VS Code", variable=vs_code, font=font_style, cursor="hand2").pack(side="left", anchor='w')
  tk.Button(vs_code_frame, text="Edit Code", command=show_vs_code_input, font=font_style, cursor="hand2").pack(side="right", padx=10)
  vs_code_frame.pack(anchor='w', pady=1)

  tk.Checkbutton(root, text="Auto Yes Bypass", variable=td_nw, font=font_style, cursor="hand2").pack(anchor='w')

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
        if vs_code.get():
          create_vs_code(code_content)
        if td_nw.get():
          td()
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
  
#python -m PyInstaller --onefile --windowed --add-data "images/not_working_final.png;images" main_app.py