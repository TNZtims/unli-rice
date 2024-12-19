import os
import json
import pymsgbox

def load_default_contents():
  documents_folder = os.path.join(os.path.expanduser("~"), "Documents", "_Unli Rice_")
  configs_path = os.path.join(documents_folder, "configs.json")

  results = {
    "report_content": "",
    "code_content": "",
    "report_path": "",
    "vs_code_path": "",
    "image_source_path": "",
    "image_destination_path": "",
    "flags": {}
  }

  try:
    configs_path = os.getenv("UNLI_RICE_CONFIG_PATH", configs_path)

    with open(configs_path, 'r', encoding='utf-8') as config_file:
      configs = json.load(config_file)
      default_report_path = configs.get("default_report", "")
      default_code_path = configs.get("default_code", "")
      image_source_path = configs.get("image_source_path", "")
      image_destination_path = configs.get("image_destination_path", "")
      flags = configs.get("flags")
      virtual_camera_delay = configs.get("virtual_camera_delay")
      results["report_path"] = default_report_path
      results["vs_code_path"] = default_code_path
      results["image_source_path"] = image_source_path
      results["image_destination_path"] = image_destination_path
      results["flags"] = flags
      results["virtual_camera_delay"] = virtual_camera_delay
  except FileNotFoundError:
    pymsgbox.alert(f"{configs_path} not found. Ensure the configuration file exists.","Missing Config File")
    return results
  except json.JSONDecodeError as e:
    pymsgbox.alert(f"Error parsing {configs_path}: {e}","Invalid Config File")
    return results
  except Exception as e:
    pymsgbox.alert(f"An error occurred while loading the configuration file: {e}","Error")
    return results

  try:
    with open(default_report_path, 'r', encoding='utf-8') as file:
      results["report_content"] = file.read()
  except FileNotFoundError:
    results["report_content"] = "Default report content not found."
    pymsgbox.alert(f"{default_report_path} not found. Using default report content.","Missing File")
  except Exception as e:
    results["report_content"] = "An error occurred while loading the default report."
    pymsgbox.alert(f"An error occurred while loading {default_report_path}: {e}","Error")

  try:
    with open(default_code_path, 'r', encoding='utf-8') as file:
      results["code_content"] = file.read()
  except FileNotFoundError:
    results["code_content"] = "Default code content not found."
    pymsgbox.alert(f"{default_code_path} not found. Using default code content.","Missing File")
  except Exception as e:
    results["code_content"] = "An error occurred while loading the default code."
    pymsgbox.alert(f"An error occurred while loading {default_code_path}: {e}","Error")

  return results