from invoke import task

@task
def build(c):
  c.run(
    'python -m PyInstaller --onefile --windowed --icon="images/unli_rice.ico" '
    '--add-data "images/unli_rice.ico;images" '
    '--add-data "images/not_working_final.png;images" '
    '--add-data "images/not_working_final_2.png;images" '
    '--add-data "images/start_working_again.png;images" '
    '--add-data "images/start_working_again_2.png;images" '
    'main_app.py'
  )
  
#python -m invoke build