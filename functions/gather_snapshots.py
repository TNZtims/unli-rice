import cv2
import time
import os
import threading
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
from utils.toast import show_toast

execution_lock = threading.Lock()

def take_webcam_shots(duration: int, interval: int, output_dir: str):
  def capture_shots():
    show_toast('Initializing Camera', 1000, "top-right", "info")
    os.makedirs(output_dir, exist_ok=True)
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
      show_toast('Error: Could not open webcam.', 1000, "top-right", "error")
      return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    start_time = time.time()
    shot_count = 0
    
    while (time.time() - start_time) < duration:
      shot_count += 1
      show_toast(f'Shot #{shot_count}', 1000, "top-right", "info")
      
      ret, frame = cap.read()
      if not ret:
        show_toast('Error: Failed to capture frame.', 1000, "top-right", "error")
        break
      
      filename = os.path.join(output_dir, f"{timestamp}_{shot_count:03d}.jpg")
      cv2.imwrite(filename, frame)
      
      time.sleep(interval)
    
    cap.release()
    cv2.destroyAllWindows()
    show_toast('Webcam shots completed!', 3000, "top-right", "info")

  with execution_lock:
    capture_shots()

def show_gather_snapshot_modal(root):
  def show_parent_window(gather_snapshot_window):
    gather_snapshot_window.destroy()
    root.deiconify()

  def validate_input(new_value):
    return new_value == "" or new_value.isdigit()

  def select_folder():
    selected_folder = filedialog.askdirectory()
    if selected_folder:
      folder_var.set(selected_folder)

  def start_snapshot_process():
    try:
      duration = int(duration_var.get())
      interval = int(interval_var.get())
      output_dir = folder_var.get()
      if not os.path.isdir(output_dir):
        show_toast('Error: Please select a valid folder.', 2000, "top-right", "error")
        return
      
      start_button.config(state="disabled", text="Processing...", background="gray", foreground="black", cursor="circle")
      gather_snapshot_window.update_idletasks()

      def complete_snapshots():
        take_webcam_shots(duration, interval, output_dir)
        start_button.config(state="normal", text="Start", background="green", foreground="white", cursor="hand2")

      threading.Thread(target=complete_snapshots, daemon=True).start()
    except ValueError:
      show_toast('Error: Invalid duration or interval value.', 2000, "top-right", "error")

  vcmd = (root.register(validate_input), '%P')
  root.withdraw()
  
  gather_snapshot_window = tk.Toplevel(root)
  gather_snapshot_window.title("Gather Snapshots")
  gather_snapshot_window.attributes("-alpha", 0.6)
  gather_snapshot_window.resizable(False, False)
  gather_snapshot_window.focus_force()

  root_x, root_y = root.winfo_x(), root.winfo_y()
  root_width, root_height = root.winfo_width(), root.winfo_height()

  gather_snapshot_window.geometry(f"{root_width}x{int(root_height/2)}+{root_x}+{root_y}")
  gather_snapshot_window.protocol("WM_DELETE_WINDOW", lambda: show_parent_window(gather_snapshot_window))

  parent_frame = tk.Frame(gather_snapshot_window)
  parent_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

  duration_frame = tk.Frame(parent_frame)
  tk.Label(duration_frame, text="Duration", font=("Arial", 12)).pack(side="left", padx=5)
  duration_var = tk.StringVar(value="60")
  duration_spinbox = tk.Spinbox(duration_frame, textvariable=duration_var, from_=0, to=999, wrap=True, increment=1, validate="key", validatecommand=vcmd, width=5, font=("Arial", 12))
  duration_spinbox.pack(side="left", padx=5)
  tk.Label(duration_frame, text="in Seconds", font=("Arial", 10)).pack(side="left", padx=5)
  duration_frame.pack(anchor='w', pady=(20, 5))

  interval_frame = tk.Frame(parent_frame)
  tk.Label(interval_frame, text="Interval", font=("Arial", 12)).pack(side="left", padx=5)
  interval_var = tk.StringVar(value="1")
  interval_spinbox = tk.Spinbox(interval_frame, textvariable=interval_var, from_=0, to=999, wrap=True, increment=1, validate="key", validatecommand=vcmd, width=5, font=("Arial", 12))
  interval_spinbox.pack(side="left", padx=5)
  tk.Label(interval_frame, text="in Seconds", font=("Arial", 10)).pack(side="left", padx=5)
  interval_frame.pack(anchor='w', pady=5)

  folder_frame = tk.Frame(parent_frame)
  folder_var = tk.StringVar(value="No folder selected")
  folder_button = tk.Button(folder_frame, text="Destination Folder", command=select_folder, font=("Arial", 12), cursor="hand2")
  folder_path_label = tk.Label(folder_frame, textvariable=folder_var, font=("Arial", 10), fg="black", anchor="w", width=40)
  folder_button.pack(side="left", padx=5)
  folder_path_label.pack(side="right", fill="x", expand=True)
  folder_frame.pack(anchor='w', pady=10)

  start_button_frame = tk.Frame(parent_frame)
  start_button_frame.place(relx=0.5, rely=1.0, anchor="s", relwidth=1.0)
  start_button = tk.Button(start_button_frame, text="Start", font=("Arial", 12, 'bold'), bg="green", fg="white", cursor="hand2", command=start_snapshot_process)
  start_button.pack(pady=10, fill="x")

  gather_snapshot_window.mainloop()