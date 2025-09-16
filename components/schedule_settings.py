import tkinter as tk
from tkinter import ttk
import re

# Modern dark theme colors (matching main_app.py and modals.py)
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

# Modern typography (matching main_app.py and modals.py)
title_font = ("Segoe UI", 16, "bold")
header_font = ("Segoe UI", 12, "bold")
body_font = ("Segoe UI", 11)
small_font = ("Segoe UI", 9)
button_font = ("Segoe UI", 12, "bold")

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
  schedule_root.title(f"📅 {key} - Schedule Editor")
  schedule_root.attributes("-alpha", 0.95)
  schedule_root.resizable(False, False)
  schedule_root.focus_force()
  schedule_root.configure(bg=DARK_BG)
  
  root_x = settings_root.winfo_x()
  root_y = settings_root.winfo_y()
  root_width = settings_root.winfo_width()
  root_height = settings_root.winfo_height()
  
  schedule_root.geometry(f"{root_width}x{root_height}+{root_x}+{root_y}")
  schedule_root.protocol("WM_DELETE_WINDOW", lambda: show_parent_window(schedule_root))
  
  # Header section
  header_frame = tk.Frame(schedule_root, bg=SURFACE_BG, height=60)
  header_frame.pack(fill="x", pady=(0, 20))
  header_frame.pack_propagate(False)
  
  title_label = tk.Label(header_frame, text=f"📅 {key} Schedule Editor", 
                        font=title_font, bg=SURFACE_BG, fg=PRIMARY_COLOR)
  title_label.place(relx=0.5, rely=0.5, anchor="center")

  # Configure ttk style for modern treeview
  style = ttk.Style()
  style.theme_use('clam')
  
  # Configure treeview styling
  style.configure('Modern.Treeview',
                  background=ACCENT_BG,
                  foreground=TEXT_PRIMARY,
                  fieldbackground=ACCENT_BG,
                  borderwidth=0,
                  relief="flat")
  
  style.configure('Modern.Treeview.Heading',
                  background=SURFACE_BG,
                  foreground=PRIMARY_COLOR,
                  borderwidth=1,
                  relief="flat",
                  font=header_font)
  
  style.map('Modern.Treeview',
            background=[('selected', PRIMARY_COLOR)],
            foreground=[('selected', DARK_BG)])
  
  # Treeview container with modern styling
  tree_frame = tk.Frame(schedule_root, bg=DARK_BG)
  tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
  
  # Instructions label
  instructions = tk.Label(tree_frame, text="💡 Double-click cells to edit • Click row to select for deletion",
                         font=small_font, fg=WARNING_COLOR, bg=DARK_BG)
  instructions.pack(pady=(0, 10))
  
  columns = ("label", "toggle", "enabled", "time")
  tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12,
                     style='Modern.Treeview')

  tree.heading("label", text="📝 Label")
  tree.heading("toggle", text="🔄 Toggle")
  tree.heading("enabled", text="✅ Enabled")
  tree.heading("time", text="⏰ Time")

  tree.column("label", width=120)
  tree.column("toggle", width=80, anchor=tk.CENTER)
  tree.column("enabled", width=80, anchor=tk.CENTER)
  tree.column("time", width=110, anchor=tk.CENTER)

  for item in value:
    tree.insert("", tk.END, values=(item["label"], str(item["toggle"]), str(item["enabled"]), item["time"]))

  tree.pack(fill=tk.BOTH, expand=True)

  time_format_regex = re.compile(r"^(0[1-9]|1[0-2]):[0-5][0-9]:[0-5][0-9] (AM|PM)$")
  
  selected_rows = []

  def on_cell_double_click(event):
    selected_item = tree.focus()
    col = tree.identify_column(event.x)
    column_index = int(col.replace("#", "")) - 1

    if selected_item and column_index >= 0:
      row_id = tree.selection()[0]
      bbox = tree.bbox(row_id, col)
      if bbox:  # Make sure bbox is valid
        x, y, width, height = bbox
        
        # Get the absolute position of the treeview within the window
        tree_x = tree.winfo_x()
        tree_y = tree.winfo_y()
        
        # Calculate absolute position accounting for parent frames
        abs_x = tree_x + x + 20
        abs_y = tree_y + y + 80

        if column_index == 0:
          current_label = tree.item(row_id, "values")[column_index]
          label_entry = tk.Text(schedule_root, height=1, width=30, font=body_font,
                               bg=ACCENT_BG, fg=TEXT_PRIMARY, relief="flat", bd=1,
                               insertbackground=PRIMARY_COLOR, highlightthickness=0)
          label_entry.place(x=abs_x, y=abs_y, width=width, height=height)
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
          time_entry = tk.Text(schedule_root, height=1, width=20, font=body_font,
                              bg=ACCENT_BG, fg=TEXT_PRIMARY, relief="flat", bd=1,
                              insertbackground=PRIMARY_COLOR, highlightthickness=0)
          time_entry.place(x=abs_x, y=abs_y, width=width, height=height)
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
      delete_btn.config(state=tk.NORMAL, bg=ERROR_COLOR, fg=TEXT_PRIMARY, cursor="hand2")
    else:
      delete_btn.config(state=tk.DISABLED, bg=ACCENT_BG, fg=TEXT_SECONDARY, cursor="arrow")

  tree.bind("<<TreeviewSelect>>", update_button_state)

  # Bottom buttons with modern styling
  btn_frame = tk.Frame(schedule_root, bg=DARK_BG)
  btn_frame.pack(fill="x", side="bottom", padx=20, pady=20)

  delete_btn = tk.Button(btn_frame, text="🗑️ Delete Row", command=delete_row, 
                        font=button_font, bg=ACCENT_BG, fg=TEXT_SECONDARY, cursor="arrow",
                        relief="flat", borderwidth=0, pady=2, state=tk.DISABLED,
                        activebackground="#ff6b7a", activeforeground=TEXT_PRIMARY)
  delete_btn.pack(side=tk.LEFT, fill='x', expand=True, padx=(0, 10))

  add_btn = tk.Button(btn_frame, text="➕ Add Row", command=add_row, 
                     font=button_font, bg=SUCCESS_COLOR, fg=DARK_BG, cursor="hand2",
                     relief="flat", borderwidth=0, pady=2,
                     activebackground="#00cc77", activeforeground=DARK_BG)
  add_btn.pack(side=tk.RIGHT, fill='x', expand=True, padx=(10, 0))

  schedule_root.mainloop()