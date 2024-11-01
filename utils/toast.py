import tkinter as tk

def show_toast(message, duration=2000, position="bottom-right", toast_type="default"):
  toast = tk.Toplevel()
  toast.overrideredirect(True)
  toast.attributes("-topmost", True)
  toast.attributes("-alpha", 0.7)

  screen_width = toast.winfo_screenwidth()
  screen_height = toast.winfo_screenheight()

  toast_width = 300
  toast_height = 50

  if position == "top-left":
    x = 10
    y = 10
  elif position == "top-right":
    x = screen_width - toast_width - 10
    y = 10
  elif position == "bottom-left":
    x = 10
    y = screen_height - toast_height - 40
  elif position == "bottom-right":
    x = screen_width - toast_width - 10
    y = screen_height - toast_height - 40
  else:
    x = screen_width - toast_width - 10
    y = screen_height - toast_height - 40

  toast.geometry(f"{toast_width}x{toast_height}+{x}+{y}")

  colors = {
    "default": "gray",
    "info": "#2196F3",
    "success": "#4CAF50",
    "warning": "#FF9800",
    "error": "#F44336"
  }
  bg_color = colors.get(toast_type, "gray")

  label = tk.Label(toast, text=message, font=("Arial", 10), bg=bg_color, fg="white", padx=10, pady=5)
  label.pack(fill="both", expand=True)

  toast.after(duration, toast.destroy)