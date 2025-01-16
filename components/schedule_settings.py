import tkinter as tk
from tkinter import ttk
import re

def open_schedule_settings(settings_root, key, value, callback):
  def get_updated_data():
    updated_data = []
    for row_id in tree.get_children():
      row_values = tree.item(row_id, "values")
      updated_data.append({
        "label": row_values[0],
        "toggle": row_values[1] == "True",
        "enabled": row_values[2] == "True",
        "time": row_values[3]
      })
    return updated_data
  
  def show_parent_window(schedule_root):
    updated_value = get_updated_data()
    schedule_root.destroy()
    settings_root.deiconify()
    callback(updated_value)
    
  settings_root.withdraw()
    
  schedule_root = tk.Toplevel(settings_root)
  schedule_root.title(f"{key} - Schedule")
  schedule_root.attributes("-alpha", 0.6)
  schedule_root.resizable(False, False)
  schedule_root.focus_force()
  
  root_x = settings_root.winfo_x()
  root_y = settings_root.winfo_y()
  root_width = settings_root.winfo_width()
  root_height = settings_root.winfo_height()
  
  schedule_root.geometry(f"{root_width}x{root_height}+{root_x}+{root_y}")
  schedule_root.protocol("WM_DELETE_WINDOW", lambda: show_parent_window(schedule_root))

  columns = ("label", "toggle", "enabled", "time")
  tree = ttk.Treeview(schedule_root, columns=columns, show="headings", height=10)

  tree.heading("label", text="Label")
  tree.heading("toggle", text="Toggle")
  tree.heading("enabled", text="Enabled")
  tree.heading("time", text="Time")

  tree.column("label", width=130)
  tree.column("toggle", width=60, anchor=tk.CENTER)
  tree.column("enabled", width=60, anchor=tk.CENTER)
  tree.column("time", width=90, anchor=tk.CENTER)

  for item in value:
    tree.insert("", tk.END, values=(item["label"], str(item["toggle"]), str(item["enabled"]), item["time"]))

  tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

  time_format_regex = re.compile(r"^(0[1-9]|1[0-2]):[0-5][0-9]:[0-5][0-9] (AM|PM)$")
  
  selected_rows = []

  def on_cell_double_click(event):
    selected_item = tree.focus()
    col = tree.identify_column(event.x)
    column_index = int(col.replace("#", "")) - 1

    if selected_item and column_index >= 0:
      row_id = tree.selection()[0]
      x, y, width, height = tree.bbox(row_id, col)

      if column_index == 0:
        current_label = tree.item(row_id, "values")[column_index]
        label_entry = tk.Text(schedule_root, height=1, width=30)
        label_entry.place(x=x, y=y + 28, width=width, height=height)
        label_entry.insert("1.0", current_label)
        label_entry.focus()

        def save_label(event=None):
          new_label = label_entry.get("1.0", tk.END).strip()
          tree.set(row_id, column=col, value=new_label)
          label_entry.destroy()

        def cancel_label(event=None):
          label_entry.destroy()

        label_entry.bind("<FocusOut>", save_label)
        label_entry.bind("<Return>", lambda event: save_label())
        label_entry.bind("<Escape>", cancel_label)

      elif column_index in (1, 2):
        current_value = tree.item(row_id, "values")[column_index] == "True"
        new_value = not current_value
        tree.set(row_id, column=col, value=str(new_value))

      elif column_index == 3:
        current_time = tree.item(row_id, "values")[column_index]
        original_time = current_time
        time_entry = tk.Text(schedule_root, height=1, width=20)
        time_entry.place(x=x, y=y + 28, width=width, height=height)
        time_entry.insert("1.0", current_time)
        time_entry.focus()

        def save_time(event=None):
          new_time = time_entry.get("1.0", tk.END).strip()
          if time_format_regex.match(new_time):
            tree.set(row_id, column=col, value=new_time)
          else:
            print("Invalid Time Format")
          time_entry.destroy()

        def cancel_time(event=None):
          time_entry.destroy()

        time_entry.bind("<FocusOut>", save_time)
        time_entry.bind("<Return>", lambda event: save_time())
        time_entry.bind("<Escape>", cancel_time)

  tree.bind("<Double-1>", on_cell_double_click)

  def delete_row():
    for selected_item in tree.selection():
      tree.delete(selected_item)
    update_button_state()

  def add_row():
    selected_item = tree.selection()
    if selected_item:
      new_row_index = tree.index(selected_item[0]) + 0
      tree.insert("", new_row_index, values=("New Label", "False", "False", "12:00:00 PM"))
    else:
      tree.insert("", tk.END, values=("New Label", "False", "False", "12:00:00 PM"))
      
  def update_button_state(*args):
    selected_rows[:] = tree.selection()
    if selected_rows:
      delete_btn.config(state=tk.NORMAL, bg="red", fg="white", cursor="hand2")
    else:
      delete_btn.config(state=tk.DISABLED, bg="gray", fg="white", cursor="arrow")

  tree.bind("<<TreeviewSelect>>", update_button_state)

  btn_frame = tk.Frame(schedule_root)
  btn_frame.pack(pady=10)

  delete_btn = tk.Button(btn_frame, text="Delete Row", command=delete_row, font=("Arial", 10, 'bold'), bg="gray", fg="white", cursor="arrow", width=10, state=tk.DISABLED)
  delete_btn.pack(side=tk.LEFT, padx=10)

  add_btn = tk.Button(btn_frame, text="Add Row", command=add_row, font=("Arial", 10, 'bold'), bg="green", fg="white", cursor="hand2", width=10)
  add_btn.pack(side=tk.LEFT, padx=10)

  schedule_root.mainloop()