import ctypes
import tkinter as tk

def get_screen_resolution_and_scale():
  root = tk.Tk()
  root.withdraw() 
  screen_width = root.winfo_screenwidth()
  screen_height = root.winfo_screenheight()
  root.destroy()

  user32 = ctypes.windll.user32
  hdc = user32.GetDC(0)
  dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)  
  user32.ReleaseDC(0, hdc)

  scale = dpi / 96 

  return {
    "resolution": {"width": screen_width, "height": screen_height},
    "scale": scale
  }
  
def calculate_dynamic_geometry(base_width, base_height, base_res, current_res, scale):
  width_scale = current_res["width"] / base_res["width"]
  height_scale = current_res["height"] / base_res["height"]
  final_width = int(base_width * width_scale * scale)
  final_height = int(base_height * height_scale * scale)
  
  return final_width, final_height

# screen_info = get_screen_resolution_and_scale()
# print(f"Screen resolution: {screen_info['resolution']['width']}x{screen_info['resolution']['height']}")
# print(f"Screen scale: {screen_info['scale']:.2f}")