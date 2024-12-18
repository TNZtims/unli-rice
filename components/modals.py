import os
import sys
import pymsgbox
import tkinter as tk
import json
from tkinter import Text, filedialog
from .get_defaults import load_default_contents

def show_report_input(root, report_content):
  report_window = tk.Toplevel(root)
  report_window.attributes("-fullscreen", True)
  report_window.title("Edit Report")
  report_text = Text(report_window, wrap='word')
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

  tk.Button( report_window, text="Save", command=save_report, cursor="hand2", font=('Arial', 12), bg="green", fg="white" ).pack(padx=20, pady=(25,0), fill='x')
  tk.Button( report_window, text="Cancel", command=cancel_changes, cursor="hand2", font=('Arial', 12), bg="red", fg="white" ).pack(padx=20, pady=(0,25), fill='x')
  report_window.wait_window()
  return updated_content["value"]

def show_vs_code_input(root, code_content):
  vs_code_window = tk.Toplevel(root)
  vs_code_window.attributes("-fullscreen", True)
  vs_code_window.title("Edit Code")
  vs_code_text = Text(vs_code_window, wrap='word')
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

  tk.Button( vs_code_window, text="Save", command=save_vs_code, cursor="hand2", font=('Arial', 12), bg="green", fg="white" ).pack(padx=20, pady=(25,0), fill='x')
  tk.Button( vs_code_window, text="Cancel", command=cancel_changes, cursor="hand2", font=('Arial', 12), bg="red", fg="white" ).pack(padx=20, pady=(0,25), fill='x')
  vs_code_window.wait_window()
  return updated_content["value"]

def open_settings(root):
  documents_folder = os.path.join(os.path.expanduser("~"), "Documents", "_Unli Rice_")
  configs_path = os.path.join(documents_folder, "configs.json")
  
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

  root.withdraw()

  default_contents = load_default_contents()
  image_source_path = default_contents["image_source_path"]
  image_destination_path = default_contents["image_destination_path"]
  minutes_default = default_contents["virtual_camera_delay"]["minutes"]
  seconds_default = default_contents["virtual_camera_delay"]["seconds"]
  flags = default_contents["flags"]

  settings_window = tk.Toplevel(root)
  settings_window.title("Configurations")
  settings_window.attributes("-alpha", 0.6)
  settings_window.resizable(False, False)
  settings_window.focus_force()

  root_x = root.winfo_x()
  root_y = root.winfo_y()
  root_width = root.winfo_width()
  root_height = root.winfo_height()

  settings_window.geometry(f"{root_width}x{root_height}+{root_x}+{root_y}")
  settings_window.protocol("WM_DELETE_WINDOW", lambda: show_parent_window(settings_window))

  font_style = ("Arial", 12)
  always_on_cam_bool = tk.BooleanVar(value=flags["camera_always_on"])
  virtual_cam_bool = tk.BooleanVar(value=flags["enable_virtual_camera"])
  snapshot_bool = tk.BooleanVar(value=flags["enable_startup_snapshot"])

  camera_settings_frame = tk.Frame(settings_window, borderwidth=1, relief="raised", bd=3)
  camera_settings_frame.pack(padx=20, pady=(20, 10), fill='x')
  camera_settings_label = tk.Label(camera_settings_frame, text="Camera", font=("Arial", 12, 'bold'), anchor="w")
  camera_settings_label.pack(padx=10, pady=5)

  always_on_cam_frame = tk.Frame(camera_settings_frame)
  tk.Checkbutton(always_on_cam_frame, text="Always On", variable=always_on_cam_bool, font=font_style, cursor="hand2").pack(side="left", anchor='w')
  always_on_cam_frame.pack(anchor='w', pady=1)
  
  enable_snapshot_frame = tk.Frame(camera_settings_frame)
  tk.Checkbutton(enable_snapshot_frame, text="Enable Snapshot at Start of Execution", variable=snapshot_bool, font=font_style, cursor="hand2").pack(side="left", anchor='w')
  enable_snapshot_frame.pack(anchor='w', pady=1)

  virtual_cam_frame = tk.Frame(camera_settings_frame)
  tk.Checkbutton(virtual_cam_frame, text="Enable Virtual Camera", variable=virtual_cam_bool, font=font_style, cursor="hand2", command=toggle_spinbox_state).pack(side="left", anchor='w')
  virtual_cam_frame.pack(anchor='w', pady=1)
  
  minutes_var = tk.StringVar(value=minutes_default)
  seconds_var = tk.StringVar(value=seconds_default)
  td_ob_frame = tk.Frame(camera_settings_frame)
  seconds_spinbox = tk.Spinbox(td_ob_frame, textvariable=seconds_var, from_=0, to=59, wrap=True, increment=1, validate="key", validatecommand=vcmd, width=5, font=font_style)
  seconds_spinbox.pack(side="right", padx=5)
  minutes_spinbox = tk.Spinbox(td_ob_frame, textvariable=minutes_var, from_=0, to=1000, wrap=True, increment=1, validate="key", validatecommand=vcmd, width=5, font=font_style)
  minutes_spinbox.pack(side="right", padx=10)
  td_ob_frame.pack(anchor='w', pady=1, padx=20)
  tk.Label(camera_settings_frame, text="* Image switching delay in minutes and seconds", font=("Arial", 8), fg="red").pack(anchor="w", pady=0, padx=30)

  locations_settings_frame = tk.Frame(settings_window, borderwidth=1, relief="raised", bd=3)
  locations_settings_frame.pack(padx=20, pady=10, fill='x')
  locations_settings_label = tk.Label(locations_settings_frame, text="Source/Destination Locations", font=("Arial", 12, 'bold'))
  locations_settings_label.pack(padx=10, pady=5)

  source_folder = tk.StringVar(value=image_source_path)
  destination_folder = tk.StringVar(value=image_destination_path)

  source_frame = tk.Frame(locations_settings_frame)
  source_frame.pack(padx=10, pady=5, anchor='w')
  source_button = tk.Button(source_frame, text="Image Source Folder", command=lambda: choose_folder(source_folder, source_label), font=font_style, cursor="hand2")
  source_button.pack(side="left", padx=5)
  source_label = tk.Label(source_frame, textvariable=source_folder, font=font_style, anchor="w")
  source_label.pack(side="left", padx=5)

  destination_frame = tk.Frame(locations_settings_frame)
  destination_frame.pack(padx=10, pady=5, anchor='w')
  destination_button = tk.Button(destination_frame, text="Image Destination Folder", command=lambda: choose_folder(destination_folder, destination_label), font=font_style, cursor="hand2")
  destination_button.pack(side="left", padx=5)
  destination_label = tk.Label(destination_frame, textvariable=destination_folder, font=font_style, anchor="w")
  destination_label.pack(side="left", padx=5)

  bottom_frame = tk.Frame(settings_window)
  bottom_frame.place(relx=0.5, rely=1.0, anchor="s")
  tk.Button(bottom_frame, text="Save", command=save_changes, font=("Arial", 12, 'bold'), bg="green", fg="white", cursor="hand2", width=10).pack(side='left', pady=20, padx=5)
  tk.Button(bottom_frame, text="Cancel", command=lambda: show_parent_window(settings_window), font=("Arial", 12, 'bold'), bg="gray", fg="white", cursor="hand2", width=10).pack(side='left', pady=20, padx=5)

  settings_window.mainloop()