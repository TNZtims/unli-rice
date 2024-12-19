import os
import cv2
import pyvirtualcam
import time
from components.get_defaults import load_default_contents
from utils.toast import show_toast

def td_shots(virtual_camera_running):
  default_contents = load_default_contents()
  image_source_path = default_contents["image_source_path"]
  virtual_camera_delay = default_contents["virtual_camera_delay"]
  
  delay_seconds = int(virtual_camera_delay.get("minutes", 0)) * 60 + int(virtual_camera_delay.get("seconds", 0))
  
  image_files = sorted([f for f in os.listdir(image_source_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

  if not image_files:
    raise FileNotFoundError(f'No image files found in {image_source_path}')

  def load_image_by_index(index):
    image_file = image_files[index]
    custom_image_path = os.path.join(image_source_path, image_file)
    image = cv2.imread(custom_image_path)
    image = cv2.resize(image, (1280, 720))
    print(f'Displaying image: {image_file}')
    show_toast(f'Displaying image: {image_file}', 3000, "top-right", "success")
    return image

  with pyvirtualcam.Camera(width=1280, height=720, fps=30) as cam:
    print(f'Virtual camera started: {cam.device}')
    show_toast(f'Virtual camera started: {cam.device}', 3000, "top-right", "info")

    current_index = 0 

    while virtual_camera_running.is_set():
      current_image = load_image_by_index(current_index)
      frame = cv2.cvtColor(current_image, cv2.COLOR_BGR2RGB)
      cam.send(frame)
      cam.sleep_until_next_frame()  
      current_index = (current_index + 1) % len(image_files)
      
      time.sleep(delay_seconds)
      
    cam.close()
    cv2.destroyAllWindows()