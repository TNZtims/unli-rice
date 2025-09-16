import os
import sys
import pymsgbox
import tkinter as tk
import json
from tkinter import Text, filedialog
from .get_defaults import load_default_contents
from .schedule_settings import open_schedule_settings

# Modern dark theme colors (matching main_app.py)
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

# Modern typography (matching main_app.py)
title_font = ("Segoe UI", 16, "bold")
header_font = ("Segoe UI", 14, "bold")
body_font = ("Segoe UI", 11)
small_font = ("Segoe UI", 9)
x_small_font = ("Segoe UI", 7)
button_font = ("Segoe UI", 12, "bold")

def show_report_input(root, report_content):
  report_window = tk.Toplevel(root)
  report_window.attributes("-fullscreen", True)
  report_window.title("📝 Edit Report")
  report_window.configure(bg=DARK_BG)
  
  # Header section
  header_frame = tk.Frame(report_window, bg=SURFACE_BG, height=60)
  header_frame.pack(fill="x", pady=(0, 20))
  header_frame.pack_propagate(False)
  
  title_label = tk.Label(header_frame, text="📝 Report Content Editor", 
                        font=title_font, bg=SURFACE_BG, fg=PRIMARY_COLOR)
  title_label.place(relx=0.5, rely=0.5, anchor="center")
  
  # Text editor with modern styling
  text_frame = tk.Frame(report_window, bg=DARK_BG)
  text_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
  
  report_text = Text(text_frame, wrap='word', font=body_font,
                    bg=ACCENT_BG, fg=TEXT_PRIMARY, 
                    insertbackground=PRIMARY_COLOR,
                    selectbackground=PRIMARY_COLOR, selectforeground=DARK_BG,
                    relief="flat", bd=0, padx=15, pady=15)
  report_text.insert(tk.END, report_content) 
  report_text.pack(fill='both', expand=True)
  updated_content = {"value": report_content}

  def save_report():
    updated_content["value"] = report_text.get("1.0", tk.END).strip()
    default_contents = load_default_contents()
    file_path = default_contents["report_path"]
    
    try:
      if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
      
      with open(file_path, "w") as report_file:
        report_file.write(updated_content["value"])
    except FileNotFoundError as e:
      pymsgbox.alert(str(e), "File Not Found")
    except Exception as e:
      pymsgbox.alert(f"An error occurred while updating the report content: {str(e)}", "Error")
    report_window.destroy() 
    
  def cancel_changes():
    report_window.destroy() 
    return

  # Bottom buttons with modern styling
  buttons_frame = tk.Frame(report_window, bg=DARK_BG)
  buttons_frame.pack(fill="x", side="bottom", padx=20, pady=20)
  
  save_button = tk.Button(buttons_frame, text="💾 Save Changes", command=save_report, 
                         cursor="hand2", font=button_font, 
                         bg=SUCCESS_COLOR, fg=DARK_BG, relief="flat", borderwidth=0, 
                         pady=12, activebackground="#00cc77", activeforeground=DARK_BG)
  save_button.pack(side="left", fill='x', expand=True, padx=(0, 10))
  
  cancel_button = tk.Button(buttons_frame, text="❌ Cancel", command=cancel_changes, 
                           cursor="hand2", font=button_font,
                           bg=ERROR_COLOR, fg=TEXT_PRIMARY, relief="flat", borderwidth=0, 
                           pady=12, activebackground="#ff6b7a", activeforeground=TEXT_PRIMARY)
  cancel_button.pack(side="right", fill='x', expand=True, padx=(10, 0))
  report_window.wait_window()
  return updated_content["value"]

def show_vs_code_input(root, code_content):
  vs_code_window = tk.Toplevel(root)
  vs_code_window.attributes("-fullscreen", True)
  vs_code_window.title("💻 Edit Code")
  vs_code_window.configure(bg=DARK_BG)
  
  # Header section
  header_frame = tk.Frame(vs_code_window, bg=SURFACE_BG, height=60)
  header_frame.pack(fill="x", pady=(0, 20))
  header_frame.pack_propagate(False)
  
  title_label = tk.Label(header_frame, text="💻 Code Content Editor", 
                        font=title_font, bg=SURFACE_BG, fg=PRIMARY_COLOR)
  title_label.place(relx=0.5, rely=0.5, anchor="center")
  
  # Text editor with modern styling
  text_frame = tk.Frame(vs_code_window, bg=DARK_BG)
  text_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
  
  vs_code_text = Text(text_frame, wrap='word', font=("Consolas", 11),
                     bg=ACCENT_BG, fg=TEXT_PRIMARY, 
                     insertbackground=PRIMARY_COLOR,
                     selectbackground=PRIMARY_COLOR, selectforeground=DARK_BG,
                     relief="flat", bd=0, padx=15, pady=15)
  vs_code_text.insert(tk.END, code_content) 
  vs_code_text.pack(fill='both', expand=True)
  updated_content = {"value": code_content}

  def save_vs_code():
    updated_content["value"] = vs_code_text.get("1.0", tk.END).strip()
    default_contents = load_default_contents()
    file_path = default_contents["vs_code_path"]
    
    try:
      if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
      
      with open(file_path, "w") as code_file:
        code_file.write(updated_content["value"])
    except FileNotFoundError as e:
      pymsgbox.alert(str(e), "File Not Found")
    except Exception as e:
      pymsgbox.alert(f"An error occurred while updating the code content: {str(e)}", "Error")
    vs_code_window.destroy()  
    
  def cancel_changes():
    vs_code_window.destroy() 
    return

  # Bottom buttons with modern styling
  buttons_frame = tk.Frame(vs_code_window, bg=DARK_BG)
  buttons_frame.pack(fill="x", side="bottom", padx=20, pady=20)
  
  save_button = tk.Button(buttons_frame, text="💾 Save Changes", command=save_vs_code, 
                         cursor="hand2", font=button_font, 
                         bg=SUCCESS_COLOR, fg=DARK_BG, relief="flat", borderwidth=0, 
                         pady=12, activebackground="#00cc77", activeforeground=DARK_BG)
  save_button.pack(side="left", fill='x', expand=True, padx=(0, 10))
  
  cancel_button = tk.Button(buttons_frame, text="❌ Cancel", command=cancel_changes, 
                           cursor="hand2", font=button_font,
                           bg=ERROR_COLOR, fg=TEXT_PRIMARY, relief="flat", borderwidth=0, 
                           pady=12, activebackground="#ff6b7a", activeforeground=TEXT_PRIMARY)
  cancel_button.pack(side="right", fill='x', expand=True, padx=(10, 0))
  vs_code_window.wait_window()
  return updated_content["value"]

def open_settings(root):
  documents_folder = os.path.join(os.path.expanduser("~"), "Documents", "_Unli Rice_")
  configs_path = os.path.join(documents_folder, "configs.json")
  configs_path = os.getenv("UNLI_RICE_CONFIG_PATH", configs_path)
  
  def load_default_contents():
    with open(configs_path, "r") as file:
      return json.load(file)

  def save_default_contents(updated_contents):
    with open(configs_path, "w") as file:
      json.dump(updated_contents, file, indent=4)

  def show_parent_window(settings_window):
    settings_window.destroy()
    root.deiconify()

  def choose_folder(var, label):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
      var.set(folder_selected)
      label.config(text=folder_selected)

  def save_changes():
    updated_contents = load_default_contents()
    updated_contents["image_source_path"] = source_folder.get()
    updated_contents["image_destination_path"] = destination_folder.get()
    updated_contents["flags"]["camera_always_on"] = always_on_cam_bool.get()
    updated_contents["flags"]["enable_virtual_camera"] = virtual_cam_bool.get()
    updated_contents["flags"]["enable_startup_snapshot"] = snapshot_bool.get()
    updated_contents["virtual_camera_delay"]["minutes"] = minutes_var.get()
    updated_contents["virtual_camera_delay"]["seconds"] = seconds_var.get()
    
    for key, new_value in updated_schedules.items():
      updated_contents["schedules"][key] = new_value
    
    save_default_contents(updated_contents)
    show_parent_window(settings_window)
    
  def validate_input(new_value):
    if new_value == "" or new_value.isdigit():
      return True
    return False
  vcmd = (root.register(validate_input), '%P')
  
  def toggle_spinbox_state():
    state = "normal" if virtual_cam_bool.get() else "disabled"
    minutes_spinbox.config(state=state)
    seconds_spinbox.config(state=state)
    
  def handle_button_schedule_click(key, value):
    def on_updated(new_value):
      updated_schedules[key] = new_value
    open_schedule_settings(settings_window, key, value, on_updated)

  root.withdraw()
  
  updated_schedules = {}

  default_contents = load_default_contents()
  image_source_path = default_contents["image_source_path"]
  image_destination_path = default_contents["image_destination_path"]
  minutes_default = default_contents["virtual_camera_delay"]["minutes"]
  seconds_default = default_contents["virtual_camera_delay"]["seconds"]
  flags = default_contents["flags"]
  schedules = default_contents["schedules"]

  settings_window = tk.Toplevel(root)
  settings_window.title("⚙️ Configurations")
  settings_window.attributes("-alpha", 0.95)
  settings_window.resizable(False, False)
  settings_window.focus_force()
  settings_window.configure(bg=DARK_BG)

  root_x = root.winfo_x()
  root_y = root.winfo_y()
  root_width = root.winfo_width()
  root_height = root.winfo_height()

  settings_window.geometry(f"{root_width}x{root_height}+{root_x}+{root_y}")
  settings_window.protocol("WM_DELETE_WINDOW", lambda: show_parent_window(settings_window))

  # Header section
  header_frame = tk.Frame(settings_window, bg=SURFACE_BG, height=60)
  header_frame.pack(fill="x", pady=(0, 20))
  header_frame.pack_propagate(False)
  
  title_label = tk.Label(header_frame, text="⚙️ System Configurations", 
                        font=title_font, bg=SURFACE_BG, fg=PRIMARY_COLOR)
  title_label.place(relx=0.5, rely=0.5, anchor="center")

  font_style = body_font
  always_on_cam_bool = tk.BooleanVar(value=flags["camera_always_on"])
  virtual_cam_bool = tk.BooleanVar(value=flags["enable_virtual_camera"])
  snapshot_bool = tk.BooleanVar(value=flags["enable_startup_snapshot"])

  # Camera settings section with modern card design
  camera_settings_frame = tk.Frame(settings_window, bg=SURFACE_BG, relief="flat", bd=0)
  camera_settings_frame.pack(padx=20, pady=(0, 15), fill='x')
  
  camera_header = tk.Frame(camera_settings_frame, bg=SURFACE_BG)
  camera_header.pack(fill="x", pady=(15, 10))
  camera_settings_label = tk.Label(camera_header, text="📷 Camera Settings", 
                                  font=header_font, bg=SURFACE_BG, fg=PRIMARY_COLOR)
  camera_settings_label.pack(side="left", padx=(15, 0))

  # Camera options with modern styling
  always_on_cam_frame = tk.Frame(camera_settings_frame, bg=SURFACE_BG)
  always_on_cam_frame.pack(anchor='w', fill='x', pady=3, padx=15)
  tk.Checkbutton(always_on_cam_frame, text="Always On", variable=always_on_cam_bool, 
                font=font_style, cursor="hand2", bg=SURFACE_BG, fg=TEXT_PRIMARY, 
                selectcolor=ACCENT_BG, activebackground=SURFACE_BG, 
                activeforeground=PRIMARY_COLOR, relief="flat", bd=0, 
                highlightthickness=0).pack(side="left", anchor='w')
  
  enable_snapshot_frame = tk.Frame(camera_settings_frame, bg=SURFACE_BG)
  enable_snapshot_frame.pack(anchor='w', fill='x', pady=3, padx=15)
  tk.Checkbutton(enable_snapshot_frame, text="Enable Snapshot at Start of Execution", 
                variable=snapshot_bool, font=font_style, cursor="hand2", 
                bg=SURFACE_BG, fg=TEXT_PRIMARY, selectcolor=ACCENT_BG, 
                activebackground=SURFACE_BG, activeforeground=PRIMARY_COLOR, 
                relief="flat", bd=0, highlightthickness=0).pack(side="left", anchor='w')

  virtual_cam_frame = tk.Frame(camera_settings_frame, bg=SURFACE_BG)
  virtual_cam_frame.pack(anchor='w', fill='x', pady=3, padx=15)
  tk.Checkbutton(virtual_cam_frame, text="Enable Virtual Camera", 
                variable=virtual_cam_bool, font=font_style, cursor="hand2", 
                command=toggle_spinbox_state, bg=SURFACE_BG, fg=TEXT_PRIMARY, 
                selectcolor=ACCENT_BG, activebackground=SURFACE_BG, 
                activeforeground=PRIMARY_COLOR, relief="flat", bd=0, 
                highlightthickness=0).pack(side="left", anchor='w')
  
  # Time delay settings
  minutes_var = tk.StringVar(value=minutes_default)
  seconds_var = tk.StringVar(value=seconds_default)
  
  delay_frame = tk.Frame(camera_settings_frame, bg=SURFACE_BG)
  delay_frame.pack(anchor='w', fill='x', pady=5, padx=15)
  
  tk.Label(delay_frame, text="Virtual Camera Delay:", font=font_style, 
           bg=SURFACE_BG, fg=TEXT_PRIMARY).pack(side="left", anchor='w')
  
  # Time picker container
  time_container = tk.Frame(delay_frame, bg=SURFACE_BG)
  time_container.pack(side="right", padx=(0, 10))
  
  minutes_spinbox = tk.Spinbox(time_container, textvariable=minutes_var, from_=0, to=1000, 
                              wrap=True, increment=1, validate="key", validatecommand=vcmd, 
                              width=5, font=font_style, justify="center",
                              bg=ACCENT_BG, fg=TEXT_PRIMARY, relief="flat", bd=1,
                              buttonbackground=ACCENT_BG, highlightthickness=0)
  minutes_spinbox.pack(side="left", padx=5)
  tk.Label(time_container, text="min", font=small_font, 
           bg=SURFACE_BG, fg=TEXT_SECONDARY).pack(side="left", padx=(0, 10))
  
  seconds_spinbox = tk.Spinbox(time_container, textvariable=seconds_var, from_=0, to=59, 
                              wrap=True, increment=1, validate="key", validatecommand=vcmd, 
                              width=5, font=font_style, justify="center",
                              bg=ACCENT_BG, fg=TEXT_PRIMARY, relief="flat", bd=1,
                              buttonbackground=ACCENT_BG, highlightthickness=0)
  seconds_spinbox.pack(side="left", padx=5)
  tk.Label(time_container, text="sec", font=small_font, 
           bg=SURFACE_BG, fg=TEXT_SECONDARY).pack(side="left")
  
  tk.Label(camera_settings_frame, text="⏱️ Image switching delay in minutes and seconds", 
           font=small_font, fg=WARNING_COLOR, bg=SURFACE_BG).pack(anchor="w", pady=(5, 15), padx=15)

  # Locations settings section with modern card design
  locations_settings_frame = tk.Frame(settings_window, bg=SURFACE_BG, relief="flat", bd=0)
  locations_settings_frame.pack(padx=20, pady=(0, 15), fill='x')
  
  locations_header = tk.Frame(locations_settings_frame, bg=SURFACE_BG)
  locations_header.pack(fill="x", pady=(15, 10))
  locations_settings_label = tk.Label(locations_header, text="📁 Source/Destination Locations", 
                                     font=header_font, bg=SURFACE_BG, fg=PRIMARY_COLOR)
  locations_settings_label.pack(side="left", padx=(15, 0))

  source_folder = tk.StringVar(value=image_source_path)
  destination_folder = tk.StringVar(value=image_destination_path)

  # Source folder section
  source_frame = tk.Frame(locations_settings_frame, bg=SURFACE_BG)
  source_frame.pack(fill='x', pady=5, padx=15)
  source_button = tk.Button(source_frame, text="📂 Image Source Folder", 
                           command=lambda: choose_folder(source_folder, source_label), 
                           font=font_style, cursor="hand2", bg=SECONDARY_COLOR, fg=DARK_BG,
                           relief="flat", borderwidth=0, padx=10, pady=0,
                           activebackground="#ff8555", activeforeground=DARK_BG)
  source_button.pack(side="left", padx=(0, 10))
  source_label = tk.Label(source_frame, textvariable=source_folder, font=small_font, 
                         bg=SURFACE_BG, fg=TEXT_SECONDARY, anchor="w")
  source_label.pack(side="left", fill='x', expand=True)

  # Destination folder section
  destination_frame = tk.Frame(locations_settings_frame, bg=SURFACE_BG)
  destination_frame.pack(fill='x', pady=5, padx=15)
  destination_button = tk.Button(destination_frame, text="📂 Image Destination Folder", 
                                command=lambda: choose_folder(destination_folder, destination_label), 
                                font=font_style, cursor="hand2", bg=SECONDARY_COLOR, fg=DARK_BG,
                                relief="flat", borderwidth=0, padx=10, pady=0,
                                activebackground="#ff8555", activeforeground=DARK_BG)
  destination_button.pack(side="left", padx=(0, 10))
  destination_label = tk.Label(destination_frame, textvariable=destination_folder, font=small_font, 
                              bg=SURFACE_BG, fg=TEXT_SECONDARY, anchor="w")
  destination_label.pack(side="left", fill='x', expand=True, pady=(0, 15))
  
  # Schedules settings section with modern card design
  schedules_settings_frame = tk.Frame(settings_window, bg=SURFACE_BG, relief="flat", bd=0)
  schedules_settings_frame.pack(padx=20, pady=(0, 15), fill='x')
  
  schedules_header = tk.Frame(schedules_settings_frame, bg=SURFACE_BG)
  schedules_header.pack(fill="x", pady=(15, 10))
  schedules_settings_label = tk.Label(schedules_header, text="📅 Schedule Management", 
                                     font=header_font, bg=SURFACE_BG, fg=PRIMARY_COLOR)
  schedules_settings_label.pack(side="left", padx=(15, 0))

  # Schedule buttons with modern styling
  for key, value in schedules.items():
    button = tk.Button(schedules_settings_frame, text=f"⏰ {key}", font=font_style, cursor="hand2", 
                      command=lambda k=key, v=value: handle_button_schedule_click(k, v),
                      bg=ACCENT_BG, fg=TEXT_PRIMARY, relief="flat", borderwidth=0,
                      pady=0, activebackground=PRIMARY_COLOR, activeforeground=DARK_BG)
    button.pack(padx=15, pady=(0, 8), fill='x')
  
  # Add padding at bottom
  tk.Frame(schedules_settings_frame, bg=SURFACE_BG, height=15).pack()

  # Bottom buttons with modern styling
  bottom_frame = tk.Frame(settings_window, bg=DARK_BG)
  bottom_frame.pack(fill="x", side="bottom", padx=20, pady=20)
  
  save_button = tk.Button(bottom_frame, text="💾 Save Configuration", command=save_changes, 
                         font=button_font, bg=PRIMARY_COLOR, fg=DARK_BG, cursor="hand2",
                         relief="flat", borderwidth=0, pady=12,
                         activebackground="#00cc77", activeforeground=DARK_BG)
  save_button.pack(side='left', fill='x', expand=True, padx=(0, 10))
  
  cancel_button = tk.Button(bottom_frame, text="❌ Cancel", 
                           command=lambda: show_parent_window(settings_window), 
                           font=button_font, bg=ERROR_COLOR, fg=TEXT_PRIMARY, cursor="hand2",
                           relief="flat", borderwidth=0, pady=12,
                           activebackground="#ff6b7a", activeforeground=TEXT_PRIMARY)
  cancel_button.pack(side='right', fill='x', expand=True, padx=(10, 0))

  settings_window.mainloop()