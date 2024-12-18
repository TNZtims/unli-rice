import cv2
import os
import time
import threading
from datetime import datetime
from .get_defaults import load_default_contents
from functions.td_shots import td_shots

def open_camera_cv2(camera_running, virtual_camera_running):
  default_contents = load_default_contents()
  camera_always_on = default_contents["flags"]["camera_always_on"]
  enable_startup_snapshot = default_contents["flags"]["enable_startup_snapshot"]
  enable_virtual_camera = default_contents["flags"]["enable_virtual_camera"]
  image_destination_path = default_contents["image_destination_path"]

  if enable_virtual_camera:
    threading.Thread( target=td_shots, args=(virtual_camera_running,), daemon=True).start()

  cap = None
  if camera_always_on:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
      return

  if not camera_always_on and not enable_virtual_camera:
    return

  image_saved = False

  os.makedirs(image_destination_path, exist_ok=True)

  while camera_running.is_set() and camera_always_on:
    ret, frame = cap.read()
    if ret and not image_saved and enable_startup_snapshot:
      timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
      filename = os.path.join(image_destination_path, f"unli_rice_{timestamp}.jpg")
      cv2.imwrite(filename, frame)
      image_saved = True

    time.sleep(1)

  if cap:
    cap.release()
  cv2.destroyAllWindows()