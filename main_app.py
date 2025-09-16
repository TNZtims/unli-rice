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
from tkinter import ttk
from PIL import Image, ImageTk
from functions.mouse_keyboard import simulate_mouse_movements, cycle_through_tabs
from functions.seller_central import go_to_seller_central_pricing_health
from functions.basecamp import go_to_basecamp
from functions.notepad import create_notepad_report
from functions.vs_code import create_vs_code
from functions.td import td
from functions.td_ob import td_ob
from functions.gather_snapshots import show_gather_snapshot_modal
from functions.td_scheduled import td_scheduled
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
schedules = default_contents["schedules"]
options = list(schedules.keys())

camera_running = threading.Event()
virtual_camera_running = threading.Event()

base_width, base_height = 500, 750
base_res = {"width": 1920, "height": 1080}
screen_info = get_screen_resolution_and_scale()
current_res = screen_info["resolution"]
scale = screen_info["scale"]
window_width, window_height = calculate_dynamic_geometry(base_width, base_height, base_res, current_res, scale)

def main():
  global report_content, code_content, label_to_use
  root = tk.Tk()
  root.title(titles["hidden"])
  root.resizable(False, False)
  root.attributes("-alpha", 0.95)  # Less transparent for modern look
  
  # Modern dark theme colors
  DARK_BG = "#1a1a1a"          # Dark background
  SURFACE_BG = "#2d2d2d"        # Elevated surface
  ACCENT_BG = "#3d3d3d"         # Interactive elements
  PRIMARY_COLOR = "#00d4ff"     # Tech blue accent
  SECONDARY_COLOR = "#ff6b35"   # Orange accent
  TEXT_PRIMARY = "#ffffff"      # White text
  TEXT_SECONDARY = "#b0b0b0"    # Gray text
  SUCCESS_COLOR = "#00ff88"     # Success green
  WARNING_COLOR = "#ffaa00"     # Warning orange
  ERROR_COLOR = "#ff4757"       # Error red
  
  # Configure root window with dark theme
  root.configure(bg=DARK_BG)
  
  screen_width = root.winfo_screenwidth()
  screen_height = root.winfo_screenheight()
  position_x = (screen_width - window_width) // 2
  position_y = (screen_height - window_height) // 2
  
  root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
  
  if hasattr(sys, "_MEIPASS"):
    icon_path = os.path.join(sys._MEIPASS, "images", "unli_rice.ico")
    gear_image_path = os.path.join(sys._MEIPASS, "images", "gear.png")
  else:
    icon_path = "images/unli_rice.ico"
    gear_image_path = "images/gear.png"
    
  root.iconbitmap(icon_path)

  # Modern typography
  title_font = ("Segoe UI", 16, "bold")
  header_font = ("Segoe UI", 14, "bold")
  body_font = ("Segoe UI", 11)
  small_font = ("Segoe UI", 9)
  x_small_font = ("Segoe UI", 7)
  button_font = ("Segoe UI", 12, "bold")
  
  font_style = body_font
  label_bool = tk.BooleanVar(value=True)
  simulate_mouse = tk.BooleanVar()
  seller_central = tk.BooleanVar()
  basecamp = tk.BooleanVar()
  cycle_tabs = tk.BooleanVar()
  notepad_report = tk.BooleanVar()
  vs_code = tk.BooleanVar()
  td_nw = tk.BooleanVar()
  td_ob_bool = tk.BooleanVar()
  collect_ss_bool = tk.BooleanVar()
  scheduled_td_bool = tk.BooleanVar()
  
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
        collect_ss_bool.set(False)
        scheduled_td_bool.set(False)
        reset_bools(False)
    elif var_name == "td_ob_bool":
      if td_ob_bool.get():
        td_nw.set(False)
        collect_ss_bool.set(False)
        scheduled_td_bool.set(False)
        reset_bools(False)
    elif var_name == "collect_ss_bool":
      if collect_ss_bool.get():
        td_ob_bool.set(False)
        td_nw.set(False)
        scheduled_td_bool.set(False)
        reset_bools(False)
    elif var_name == "scheduled_td_bool":
      if scheduled_td_bool.get():
        td_ob_bool.set(False)
        td_nw.set(False)
        collect_ss_bool.set(False)
        reset_bools(False)
    else:
      td_ob_bool.set(False)
      td_nw.set(False)
      collect_ss_bool.set(False)
      scheduled_td_bool.set(False)

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
    collect_ss_checkbox.config(text=label_to_use["collect_ss_bool_label"])
    scheduled_td_checkbox.config(text=label_to_use["scheduled_td_label"])
    
    new_title = titles["exposed"] if flag else titles["hidden"]
    root.title(new_title)

  # Header section with complete background
  header_frame = tk.Frame(root, bg=SURFACE_BG, height=70)
  header_frame.pack(fill="x", pady=(0, 20))
  header_frame.pack_propagate(False)
  
  # Title label centered in header
  menu_label = tk.Label(header_frame, text="⚡ IT Department Tool Automations", 
                       font=title_font, cursor="hand2", 
                       bg=SURFACE_BG, fg=PRIMARY_COLOR)
  menu_label.place(relx=0.45, rely=0.5, anchor="center")
  menu_label.bind("<Button-1>", lambda event: toggle_labels(label_bool.get()))

  # Settings button positioned within header frame
  settings_button = tk.Button(header_frame, text="⚙", font=("Segoe UI", 16),
                             command=lambda: open_settings(root), 
                             bg=ACCENT_BG, fg=TEXT_PRIMARY,
                             relief="flat", borderwidth=0, cursor="hand2",
                             width=3, height=1,
                             activebackground=PRIMARY_COLOR,
                             activeforeground=DARK_BG)
  settings_button.place(relx=1.0, rely=0.5, anchor="e", x=-15)

  # Main options section
  main_frame = tk.Frame(root, bg=DARK_BG)
  main_frame.pack(fill="x", padx=20, pady=(0, 15))
  
  simulate_checkbox = tk.Checkbutton(main_frame, text=label_to_use["simulate_mouse_label"], 
                                   variable=simulate_mouse, font=body_font, cursor="hand2", 
                                   command=lambda: toggle_checkboxes("simulate_mouse"),
                                   bg=DARK_BG, fg=TEXT_PRIMARY, selectcolor=ACCENT_BG,
                                   activebackground=DARK_BG, activeforeground=PRIMARY_COLOR,
                                   relief="flat", bd=0, highlightthickness=0)
  simulate_checkbox.pack(anchor='w', pady=5)

  # Seller Central section
  seller_frame = tk.Frame(main_frame, bg=DARK_BG)
  seller_frame.pack(anchor='w', fill='x', pady=2)
  seller_checkbox = tk.Checkbutton(seller_frame, text=label_to_use["seller_central_label"], 
                                 variable=seller_central, font=body_font, cursor="hand2", 
                                 command=lambda: toggle_checkboxes("seller_central"),
                                 bg=DARK_BG, fg=TEXT_PRIMARY, selectcolor=ACCENT_BG,
                                 activebackground=DARK_BG, activeforeground=PRIMARY_COLOR,
                                 relief="flat", bd=0, highlightthickness=0)
  seller_checkbox.pack(anchor='w')
  tk.Label(seller_frame, text="⚠ Ensure your Seller Central is logged in", 
           font=small_font, fg=WARNING_COLOR, bg=DARK_BG).pack(anchor="w", padx=20)

  # Basecamp section  
  basecamp_frame = tk.Frame(main_frame, bg=DARK_BG)
  basecamp_frame.pack(anchor='w', fill='x', pady=2)
  basecamp_checkbox = tk.Checkbutton(basecamp_frame, text=label_to_use["basecamp_label"], 
                                   variable=basecamp, font=body_font, cursor="hand2", 
                                   command=lambda: toggle_checkboxes("basecamp"),
                                   bg=DARK_BG, fg=TEXT_PRIMARY, selectcolor=ACCENT_BG,
                                   activebackground=DARK_BG, activeforeground=PRIMARY_COLOR,
                                   relief="flat", bd=0, highlightthickness=0)
  basecamp_checkbox.pack(anchor='w')
  tk.Label(basecamp_frame, text="⚠ Ensure your Basecamp is logged in", 
           font=small_font, fg=WARNING_COLOR, bg=DARK_BG).pack(anchor="w", padx=20)

  cycle_checkbox = tk.Checkbutton(main_frame, text=label_to_use["cycle_tabs_label"], 
                                variable=cycle_tabs, font=body_font, cursor="hand2", 
                                command=lambda: toggle_checkboxes("cycle_tabs"),
                                bg=DARK_BG, fg=TEXT_PRIMARY, selectcolor=ACCENT_BG,
                                activebackground=DARK_BG, activeforeground=PRIMARY_COLOR,
                                relief="flat", bd=0, highlightthickness=0)
  cycle_checkbox.pack(anchor='w', pady=5)

  # Notepad section with modern styling
  notepad_frame = tk.Frame(main_frame, bg=DARK_BG)
  notepad_frame.pack(anchor='w', fill='x', pady=5)
  notepad_checkbox = tk.Checkbutton(notepad_frame, text=label_to_use["notepad_report_label"], 
                                  variable=notepad_report, font=body_font, cursor="hand2", 
                                  command=lambda: toggle_checkboxes("notepad_report"),
                                  bg=DARK_BG, fg=TEXT_PRIMARY, selectcolor=ACCENT_BG,
                                  activebackground=DARK_BG, activeforeground=PRIMARY_COLOR,
                                  relief="flat", bd=0, highlightthickness=0)
  notepad_checkbox.pack(side="left", anchor='w')
  
  edit_report_btn = tk.Button(notepad_frame, text="📝 Edit Report", 
                             command=lambda: update_report_content(show_report_input(root, report_content)), 
                             font=small_font, cursor="hand2",
                             bg=SECONDARY_COLOR, fg=DARK_BG, relief="flat", 
                             borderwidth=0, padx=12, pady=4,
                             activebackground="#ff8555", activeforeground=DARK_BG)
  edit_report_btn.pack(side="right", padx=(10, 0))

  # VS Code section with modern styling
  vs_code_frame = tk.Frame(main_frame, bg=DARK_BG)
  vs_code_frame.pack(anchor='w', fill='x', pady=5)
  vs_code_checkbox = tk.Checkbutton(vs_code_frame, text=label_to_use["vs_code_label"], 
                                  variable=vs_code, font=body_font, cursor="hand2", 
                                  command=lambda: toggle_checkboxes("vs_code"),
                                  bg=DARK_BG, fg=TEXT_PRIMARY, selectcolor=ACCENT_BG,
                                  activebackground=DARK_BG, activeforeground=PRIMARY_COLOR,
                                  relief="flat", bd=0, highlightthickness=0)
  vs_code_checkbox.pack(side="left", anchor='w')
  
  edit_code_btn = tk.Button(vs_code_frame, text="💻 Edit Code", 
                           command=lambda: update_code_content(show_vs_code_input(root, code_content)), 
                           font=small_font, cursor="hand2",
                           bg=SECONDARY_COLOR, fg=DARK_BG, relief="flat", 
                           borderwidth=0, padx=12, pady=4,
                           activebackground="#ff8555", activeforeground=DARK_BG)
  edit_code_btn.pack(side="right", padx=(10, 0))

  # Advanced options section with modern card design
  group_frame = tk.Frame(root, bg=SURFACE_BG, relief="flat", bd=0) 
  group_frame.pack(anchor="w", fill="x", pady=(20, 20), padx=20)
  
  # Header for advanced section
  advanced_header = tk.Frame(group_frame, bg=SURFACE_BG)
  advanced_header.pack(fill="x", pady=(15, 10))
  tk.Label(advanced_header, text="🔧 Advanced Options", font=header_font, 
           bg=SURFACE_BG, fg=PRIMARY_COLOR).pack(side="left", padx=(15, 0))
  tk.Label(advanced_header, text="⚠ Exclusive - Cannot combine with basic options", 
           font=x_small_font, fg=ERROR_COLOR, bg=SURFACE_BG).pack(side="left", padx=(0, 15))
  
  # Configure ttk style for modern comboboxes
  style = ttk.Style()
  style.theme_use('clam')
  
  # Configure combobox styling
  style.configure('Modern.TCombobox', 
                  fieldbackground=ACCENT_BG,
                  background=ACCENT_BG,
                  foreground=TEXT_PRIMARY,
                  borderwidth=1,
                  relief="flat",
                  arrowcolor=TEXT_PRIMARY,
                  darkcolor=ACCENT_BG,
                  lightcolor=ACCENT_BG,
                  bordercolor=ACCENT_BG,
                  focuscolor="none",
                  selectbackground=PRIMARY_COLOR,
                  selectforeground=DARK_BG)
                  
  # Configure combobox dropdown
  style.map('Modern.TCombobox',
            fieldbackground=[('readonly', ACCENT_BG),
                           ('focus', ACCENT_BG)],
            background=[('readonly', ACCENT_BG),
                       ('focus', ACCENT_BG)],
            foreground=[('readonly', TEXT_PRIMARY),
                       ('focus', TEXT_PRIMARY)],
            arrowcolor=[('readonly', TEXT_PRIMARY),
                       ('focus', PRIMARY_COLOR)])
  
  # Configure dropdown list styling
  root.option_add('*TCombobox*Listbox.selectBackground', PRIMARY_COLOR)
  root.option_add('*TCombobox*Listbox.selectForeground', DARK_BG)
  root.option_add('*TCombobox*Listbox.background', ACCENT_BG)
  root.option_add('*TCombobox*Listbox.foreground', TEXT_PRIMARY)
  
  td_nw_frame = tk.Frame(group_frame, bg=SURFACE_BG)
  td_nw_frame.pack(anchor='w', fill='x', pady=5, padx=15)
  td_nw_checkbox = tk.Checkbutton(td_nw_frame, text=label_to_use["td_nw_label"], 
                                variable=td_nw, font=body_font, cursor="hand2", 
                                command=lambda: toggle_checkboxes("td_nw"),
                                bg=SURFACE_BG, fg=TEXT_PRIMARY, selectcolor=ACCENT_BG,
                                activebackground=SURFACE_BG, activeforeground=PRIMARY_COLOR,
                                relief="flat", bd=0, highlightthickness=0)
  td_nw_checkbox.pack(side='left', anchor='w')
  
  td_nw_dropdown = ttk.Combobox(td_nw_frame, values=['Wait', 'Do not wait'], 
                               state="readonly", font=body_font, 
                               style='Modern.TCombobox', width=12)
  td_nw_dropdown.pack(side='right', padx=(0, 10))
  td_nw_dropdown.set("Wait")
  
  hours_var = tk.StringVar(value="0")
  minutes_var = tk.StringVar(value="9")
  seconds_var = tk.StringVar(value="0")
  
  td_ob_frame = tk.Frame(group_frame, bg=SURFACE_BG)
  td_ob_frame.pack(anchor='w', fill='x', pady=5, padx=15)
  td_ob_checkbox = tk.Checkbutton(td_ob_frame, text=label_to_use["td_ob_bool_label"], 
                                variable=td_ob_bool, font=body_font, cursor="hand2", 
                                command=lambda: toggle_checkboxes("td_ob_bool"),
                                bg=SURFACE_BG, fg=TEXT_PRIMARY, selectcolor=ACCENT_BG,
                                activebackground=SURFACE_BG, activeforeground=PRIMARY_COLOR,
                                relief="flat", bd=0, highlightthickness=0)
  td_ob_checkbox.pack(side="left", anchor='w')
  
  # Time picker container
  time_container = tk.Frame(td_ob_frame, bg=SURFACE_BG)
  time_container.pack(side="right", padx=(0, 10))
  
  # Hours
  hours_spinbox = tk.Spinbox(time_container, textvariable=hours_var, from_=0, to=999, 
                            wrap=True, increment=1, validate="key", validatecommand=vcmd, 
                            width=4, font=body_font, justify="center",
                            bg=ACCENT_BG, fg=TEXT_PRIMARY, relief="flat", bd=1,
                            buttonbackground=ACCENT_BG, highlightthickness=0)
  hours_spinbox.pack(side="left", padx=2)
  tk.Label(time_container, text=":", font=(body_font[0], 14, 'bold'), 
           bg=SURFACE_BG, fg=PRIMARY_COLOR).pack(side="left")
  
  # Minutes  
  minutes_spinbox = tk.Spinbox(time_container, textvariable=minutes_var, from_=0, to=59, 
                              wrap=True, increment=1, validate="key", validatecommand=vcmd, 
                              width=4, font=body_font, justify="center",
                              bg=ACCENT_BG, fg=TEXT_PRIMARY, relief="flat", bd=1,
                              buttonbackground=ACCENT_BG, highlightthickness=0)
  minutes_spinbox.pack(side="left", padx=2)
  tk.Label(time_container, text=":", font=(body_font[0], 14, 'bold'), 
           bg=SURFACE_BG, fg=PRIMARY_COLOR).pack(side="left")
  
  # Seconds
  seconds_spinbox = tk.Spinbox(time_container, textvariable=seconds_var, from_=0, to=59, 
                              wrap=True, increment=1, validate="key", validatecommand=vcmd, 
                              width=4, font=body_font, justify="center",
                              bg=ACCENT_BG, fg=TEXT_PRIMARY, relief="flat", bd=1,
                              buttonbackground=ACCENT_BG, highlightthickness=0)
  seconds_spinbox.pack(side="left", padx=2)
  
  # Collect screenshots option
  collect_ss_checkbox = tk.Checkbutton(group_frame, text=label_to_use["collect_ss_bool_label"], 
                                     variable=collect_ss_bool, font=body_font, cursor="hand2", 
                                     command=lambda: toggle_checkboxes("collect_ss_bool"),
                                     bg=SURFACE_BG, fg=TEXT_PRIMARY, selectcolor=ACCENT_BG,
                                     activebackground=SURFACE_BG, activeforeground=PRIMARY_COLOR,
                                     relief="flat", bd=0, highlightthickness=0)
  collect_ss_checkbox.pack(anchor='w', pady=5, padx=15)
  
  # Scheduled option
  schedule_frame = tk.Frame(group_frame, bg=SURFACE_BG)
  schedule_frame.pack(anchor='w', fill='x', pady=5, padx=15)
  scheduled_td_checkbox = tk.Checkbutton(schedule_frame, text=label_to_use["scheduled_td_label"], 
                                       variable=scheduled_td_bool, font=body_font, cursor="hand2", 
                                       command=lambda: toggle_checkboxes("scheduled_td_bool"),
                                       bg=SURFACE_BG, fg=TEXT_PRIMARY, selectcolor=ACCENT_BG,
                                       activebackground=SURFACE_BG, activeforeground=PRIMARY_COLOR,
                                       relief="flat", bd=0, highlightthickness=0)
  scheduled_td_checkbox.pack(side='left', anchor='w')
  
  schedule_dropdown = ttk.Combobox(schedule_frame, values=options, state="readonly", 
                                 font=body_font, style='Modern.TCombobox', width=15)
  schedule_dropdown.pack(side='right', padx=(0, 10))
  schedule_dropdown.set("Select an option")
  
  if options: 
    schedule_dropdown.set(options[0])
  
  # Footer note for advanced section with proper spacing
  footer_note = tk.Label(group_frame, text="⌨️ Ensure keyboard shortcut is enabled", 
                        font=small_font, fg=WARNING_COLOR, bg=SURFACE_BG)
  footer_note.pack(anchor="w", pady=(10, 20), padx=15)

  def execute_selected_thread():
    def validate_selection():
      if not (simulate_mouse.get() or seller_central.get() or basecamp.get() or cycle_tabs.get() or notepad_report.get() or vs_code.get() or td_nw.get() or td_ob_bool.get() or collect_ss_bool.get() or scheduled_td_bool.get()):
        pymsgbox.alert(text="Please select at least one task before starting.", title="No Task Selected", button="OK")
        return False
      return True

    if not validate_selection():
      return
    if collect_ss_bool.get():
      root.after(0, show_gather_snapshot_modal, root)
      return
    result = pymsgbox.confirm(text='Run the selected tasks in a loop? Make sure that the next active tab is your browser', title='Confirm', buttons=['OK', 'Cancel'])
    if result == 'Cancel':
      return
    
    root.withdraw()
    show_toast("Processing...", 3000, "top-right", "info")
    print('Reloaded configs')
    default_contents = load_default_contents()
    schedules = default_contents["schedules"]

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
          td(td_nw_dropdown.get())
        if td_ob_bool.get():
          hours_value = hours_var.get()
          minutes_value = minutes_var.get()
          seconds_value = seconds_var.get()
          td_ob(hours_value, minutes_value, seconds_value)
          td_ob_bool.set(False)
          td_nw.set(True)
        if scheduled_td_bool.get():
          selected_schedule = schedule_dropdown.get()
          last_toggle = td_scheduled(selected_schedule, schedules[selected_schedule])
          print(last_toggle)
          
          if last_toggle:
            scheduled_td_bool.set(False)
            td_nw.set(True)
          else:
            break
          
    except Exception as e:
      show_toast("Script successfully stopped", 5000, "top-right", "success")
      print(f"An error occurred: {e}")
    finally:
      root.deiconify() 
      camera_running.clear()
      virtual_camera_running.clear()
      camera_thread.join()

  # Bottom section with modern start button
  bottom_frame = tk.Frame(root, bg=DARK_BG)
  bottom_frame.pack(fill="x", side="bottom", pady=(10, 0))
  
  # Start button with modern styling
  start_button = tk.Button(bottom_frame, text="🚀 START AUTOMATION", 
                          command=lambda: threading.Thread(target=execute_selected_thread, daemon=True).start(), 
                          font=button_font, bg=PRIMARY_COLOR, fg=DARK_BG, cursor="hand2",
                          relief="flat", borderwidth=0, pady=10, 
                          activebackground="#00cc77", activeforeground=DARK_BG)
  start_button.pack(pady=(0, 10), padx=20, fill='x')
  
  # Footer note with modern styling
  footer_frame = tk.Frame(bottom_frame, bg=DARK_BG)
  footer_frame.pack(fill="x", padx=20, pady=(0, 15))
  tk.Label(footer_frame, text="💡 Tip: Move cursor to top-left corner to emergency stop", 
           font=small_font, fg=TEXT_SECONDARY, bg=DARK_BG, 
           justify="center").pack()
  root.mainloop()

if __name__ == "__main__":
  try:
    main()
  finally:
    win32api.CloseHandle(handle)