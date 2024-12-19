import sys
import os
import pyautogui
import pymsgbox
import threading
import time
import win32event
import win32api
import winerror
import tkinter as tk
from PIL import Image, ImageTk
from functions.mouse_keyboard import simulate_mouse_movements, cycle_through_tabs
from functions.seller_central import go_to_seller_central_pricing_health
from functions.basecamp import go_to_basecamp
from functions.notepad import create_notepad_report
from functions.vs_code import create_vs_code
from functions.td import td
from functions.td_ob import td_ob
from functions.td_shots import td_shots
from utils.dictionaries import labels_hidden, labels_exposed, titles
from utils.toast import show_toast
from utils.screen_resolution import get_screen_resolution_and_scale, calculate_dynamic_geometry
from components.modals import show_report_input, show_vs_code_input, open_settings
from components.camera_vision import open_camera_cv2
from components.get_defaults import load_default_contents

pyautogui.PAUSE = 0.2

IT_TOOLS = "IT_TOOLS"

handle = win32event.CreateMutex(None, False, IT_TOOLS)

if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
  root = tk.Tk()
  print("Another instance of the application is already running.")
  pymsgbox.alert(text="Another instance of the application is already running.", title="Error", button="OK")
  sys.exit(1)

default_contents = load_default_contents()
report_content = default_contents["report_content"]
code_content = default_contents["code_content"]
camera_running = threading.Event()
virtual_camera_running = threading.Event()

base_width, base_height = 500, 460
base_res = {"width": 1920, "height": 1080}
screen_info = get_screen_resolution_and_scale()
current_res = screen_info["resolution"]
scale = screen_info["scale"]
dynamic_geometry = calculate_dynamic_geometry(base_width, base_height, base_res, current_res, scale)

def main():
  global report_content, code_content, label_to_use
  root = tk.Tk()
  root.title(titles["hidden"])
  root.geometry(dynamic_geometry)
  root.resizable(False, False)
  root.attributes("-alpha", 0.6)
  
  if hasattr(sys, "_MEIPASS"):
    icon_path = os.path.join(sys._MEIPASS, "images", "unli_rice.ico")
    gear_image_path = os.path.join(sys._MEIPASS, "images", "gear.png")
  else:
    icon_path = "images/unli_rice.ico"
    gear_image_path = "images/gear.png"
    
  root.iconbitmap(icon_path)

  font_style = ("Arial", 12)
  label_bool = tk.BooleanVar(value=True)
  simulate_mouse = tk.BooleanVar()
  seller_central = tk.BooleanVar()
  basecamp = tk.BooleanVar()
  cycle_tabs = tk.BooleanVar()
  notepad_report = tk.BooleanVar()
  vs_code = tk.BooleanVar()
  td_nw = tk.BooleanVar()
  td_ob_bool = tk.BooleanVar()
  
  label_to_use = labels_hidden if label_bool.get() else labels_exposed

  def validate_input(new_value):
    if new_value == "" or new_value.isdigit():
      return True
    return False
  vcmd = (root.register(validate_input), '%P')

  def update_report_content(updated_content):
    global report_content
    report_content = updated_content

  def update_code_content(new_content):
    global code_content
    code_content = new_content

  def toggle_checkboxes(var_name):
    def reset_bools(new_bool):
      simulate_mouse.set(new_bool)
      seller_central.set(new_bool)
      basecamp.set(new_bool)
      cycle_tabs.set(new_bool)
      notepad_report.set(new_bool)
      vs_code.set(new_bool)
    
    if var_name == "td_nw":
      if td_nw.get():
        td_ob_bool.set(False)
        reset_bools(False)
    elif var_name == "td_ob_bool":
      if td_ob_bool.get():
        td_nw.set(False)
        reset_bools(False)
    else:
      td_ob_bool.set(False)
      td_nw.set(False)

  def toggle_labels(flag):
    global label_to_use
    label_to_use = labels_exposed if flag else labels_hidden
    label_bool.set(not flag)
    
    simulate_checkbox.config(text=label_to_use["simulate_mouse_label"])
    seller_checkbox.config(text=label_to_use["seller_central_label"])
    basecamp_checkbox.config(text=label_to_use["basecamp_label"])
    cycle_checkbox.config(text=label_to_use["cycle_tabs_label"])
    notepad_checkbox.config(text=label_to_use["notepad_report_label"])
    vs_code_checkbox.config(text=label_to_use["vs_code_label"])
    td_nw_checkbox.config(text=label_to_use["td_nw_label"])
    td_ob_checkbox.config(text=label_to_use["td_ob_bool_label"])
    
    new_title = titles["exposed"] if flag else titles["hidden"]
    root.title(new_title)

  menu_label = tk.Label(root, text="Menu Selection:", font=("Arial", 14), cursor="hand2")
  menu_label.pack(pady=15)
  menu_label.bind("<Button-1>", lambda event: toggle_labels(label_bool.get()))

  frame = tk.Frame(root)
  frame.place(relx=1.0, rely=0.0, anchor="ne")

  gear_image = Image.open(gear_image_path).resize((30, 30))
  gear_icon = ImageTk.PhotoImage(gear_image)
  gear_button = tk.Button( frame, image=gear_icon, command=lambda: open_settings(root), borderwidth=0, cursor="hand2" )
  gear_button.pack(padx=10, pady=10)

  simulate_checkbox = tk.Checkbutton(root, text=label_to_use["simulate_mouse_label"], variable=simulate_mouse, font=font_style, cursor="hand2", command=lambda: toggle_checkboxes("simulate_mouse"))
  simulate_checkbox.pack(anchor='w', padx=20)

  seller_checkbox = tk.Checkbutton(root, text=label_to_use["seller_central_label"], variable=seller_central, font=font_style, cursor="hand2", command=lambda: toggle_checkboxes("seller_central"))
  seller_checkbox.pack(anchor='w', padx=20)
  tk.Label(root, text="* Ensure your Seller Central is logged in", font=("Arial", 8), fg="red").pack(anchor="w", pady=0, padx=30)

  basecamp_checkbox = tk.Checkbutton(root, text=label_to_use["basecamp_label"], variable=basecamp, font=font_style, cursor="hand2", command=lambda: toggle_checkboxes("basecamp"))
  basecamp_checkbox.pack(anchor='w', padx=20)
  tk.Label(root, text="* Ensure your Basecamp is logged in", font=("Arial", 8), fg="red").pack(anchor="w", pady=0, padx=30)

  cycle_checkbox = tk.Checkbutton(root, text=label_to_use["cycle_tabs_label"], variable=cycle_tabs, font=font_style, cursor="hand2", command=lambda: toggle_checkboxes("cycle_tabs"))
  cycle_checkbox.pack(anchor='w', padx=20)

  notepad_frame = tk.Frame(root)
  notepad_checkbox = tk.Checkbutton(notepad_frame, text=label_to_use["notepad_report_label"], variable=notepad_report, font=font_style, cursor="hand2", command=lambda: toggle_checkboxes("notepad_report"))
  notepad_checkbox.pack(side="left", anchor='w')
  tk.Button(notepad_frame, text="Edit Report", command=lambda: update_report_content(show_report_input(root, report_content)), font=font_style, cursor="hand2").pack(side="right", padx=10)
  notepad_frame.pack(anchor='w', pady=1, padx=20)

  vs_code_frame = tk.Frame(root)
  vs_code_checkbox = tk.Checkbutton(vs_code_frame, text=label_to_use["vs_code_label"], variable=vs_code, font=font_style, cursor="hand2", command=lambda: toggle_checkboxes("vs_code"))
  vs_code_checkbox.pack(side="left", anchor='w')
  tk.Button( vs_code_frame, text="Edit Code", command=lambda: update_code_content(show_vs_code_input(root, code_content)), font=font_style, cursor="hand2" ).pack(side="right", padx=10)
  vs_code_frame.pack(anchor='w', pady=1, padx=20)

  td_nw_checkbox = tk.Checkbutton(root, text=label_to_use["td_nw_label"], variable=td_nw, font=font_style, cursor="hand2", command=lambda: toggle_checkboxes("td_nw"))
  td_nw_checkbox.pack(anchor='w', padx=20)

  minutes_var = tk.StringVar(value="9")
  seconds_var = tk.StringVar(value="0")
  td_ob_frame = tk.Frame(root)
  td_ob_checkbox = tk.Checkbutton(td_ob_frame, text=label_to_use["td_ob_bool_label"], variable=td_ob_bool, font=font_style, cursor="hand2", command=lambda: toggle_checkboxes("td_ob_bool"))
  td_ob_checkbox.pack(side="left", anchor='w')
  tk.Spinbox(td_ob_frame, textvariable=seconds_var, from_=0, to=59, wrap=True, increment=1, validate="key", validatecommand=vcmd, width=5, font=font_style).pack(side="right", padx=5)
  tk.Spinbox(td_ob_frame, textvariable=minutes_var, from_=3, to=1000, wrap=True, increment=1, validate="key", validatecommand=vcmd, width=5, font=font_style).pack(side="right", padx=10)
  td_ob_frame.pack(anchor='w', pady=1, padx=20)
  tk.Label(root, text="* Cannot be selected along with other choices", font=("Arial", 8), fg="red").pack(anchor="w", pady=0, padx=30)

  def execute_selected_thread():
    def validate_selection():
      if not (simulate_mouse.get() or seller_central.get() or basecamp.get() or cycle_tabs.get() or notepad_report.get() or vs_code.get() or td_nw.get() or td_ob_bool.get()):
        pymsgbox.alert(text="Please select at least one task before starting.", title="No Task Selected", button="OK")
        return False
      return True

    if not validate_selection():
      return
    result = pymsgbox.confirm(text='Run the selected tasks in a loop? Make sure that the next active tab is your browser', title='Confirm', buttons=['OK', 'Cancel'])
    if result == 'Cancel':
      return
    
    root.withdraw()
    show_toast("Processing...", 3000, "top-right", "info")

    try:
      global camera_running, virtual_camera_running
      camera_running.set()
      virtual_camera_running.set()
      camera_thread = threading.Thread(target=open_camera_cv2, args=(camera_running, virtual_camera_running,), daemon=True)
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
        if td_ob_bool.get():
          minutes_value = minutes_var.get()
          seconds_value = seconds_var.get()
          td_ob(minutes_value, seconds_value)
          td_ob_bool.set(False)
          td_nw.set(True)
    except Exception as e:
      show_toast("Script successfully stopped", 5000, "top-right", "success")
      print(f"An error occurred: {e}")
    finally:
      root.deiconify() 
      camera_running.clear()
      virtual_camera_running.clear()
      camera_thread.join()

  bottom_frame = tk.Frame(root)
  bottom_frame.place(relx=0.5, rely=1.0, anchor="s")
  tk.Button(bottom_frame, text="Start", command=lambda: threading.Thread(target=execute_selected_thread, daemon=True).start(), font=("Arial", 14, 'bold'), bg="green", fg="white", cursor="hand2").pack(pady=(0, 0), padx=20, fill='x')
  tk.Label(bottom_frame, text="Note: Move your cursor to top-left most part of your main screen to force stop", font=("Arial", 10, 'bold'), fg='red').pack(pady=(0, 0))
  root.mainloop()

if __name__ == "__main__":
  try:
    main()
  finally:
    win32api.CloseHandle(handle)