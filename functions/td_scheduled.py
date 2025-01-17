import pyautogui
import time
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from utils.toast import show_toast

pyautogui.FAILSAFE = True
stop_flag = False
jobs_executed = set()
last_td_toggle = None

def td_job(job_id, job_label, td_toggle):
  global last_td_toggle
  show_toast(f"{job_label}: {td_toggle}", 2000, "top-right", "info")

  if td_toggle:
    pyautogui.hotkey('ctrl', 'alt', 'c')
    # print("PLAY")
    time.sleep(1)
  else:
    pyautogui.hotkey('ctrl', 'alt', 'b')
    # print("STOP")
    time.sleep(1)

  jobs_executed.add(job_id) 
  last_td_toggle = td_toggle

def initiate_cron_jobs(schedule):
  scheduler = BackgroundScheduler()

  for item in schedule:
    if item['enabled']:
      job_time = datetime.strptime(item['time'], "%I:%M:%S %p")
      hour = job_time.hour
      minute = job_time.minute
      second = job_time.second

      job_id = item['label'] 
      scheduler.add_job(td_job, 'cron', args=[job_id, item['label'], item['toggle']], id=job_id, hour=hour, minute=minute, second=second)
      # print(f"Scheduled job '{item['label']}' at {hour:02d}:{minute:02d}:{second:02d}")

  scheduler.start()
  return scheduler

def td_scheduled(selected_schedule, schedule):
  global stop_flag, last_td_toggle
  
  stop_flag = False
  jobs_executed.clear()
  last_td_toggle = None
  
  scheduler = initiate_cron_jobs(schedule)

  try:
    while not stop_flag:
      if pyautogui.position() == (0, 0):
        stop_flag = True

      all_jobs = {job.id for job in scheduler.get_jobs()}
      if all_jobs == jobs_executed:
        stop_flag = True

      time.sleep(1)
  except KeyboardInterrupt:
    pass
  finally:
    scheduler.shutdown(wait=False)
    show_toast("Script successfully stopped", 5000, "top-right", "success")
    return last_td_toggle