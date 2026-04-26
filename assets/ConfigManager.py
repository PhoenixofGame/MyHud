#----------------------------------------------------------------------------------------------#
#----------------------------------- Made by Phönix -------------------------------------------#
#----------------------------------------------------------------------------------------------#
import json
import os
import sys
import shutil

class ConfigManager:
    def __init__(self):
        self.appdata = os.path.join(os.environ["APPDATA"], "MyHudConfigs")
        os.makedirs(self.appdata, exist_ok=True)

    def get_config_path(self, config_name):
        filename = os.path.basename(config_name)
        appdata_path = os.path.join(self.appdata, filename)

        if not os.path.exists(appdata_path):
            if getattr(sys, 'frozen', False):
                exe_dir = os.path.dirname(sys.executable)
                # Prüfe ob wir in assets/ sind (Sub-EXEs)
                if os.path.basename(exe_dir).lower() == "assets":
                    exe_dir = os.path.dirname(exe_dir)
                default = os.path.join(exe_dir, "assets", filename)
            else:
                default = config_name
            if os.path.exists(default):
                shutil.copy(default, appdata_path)

        return appdata_path

    def clear_config(self, config_name):
        path = self.get_config_path(config_name)
        with open(path, 'w') as f:
            json.dump({}, f, indent=4)

    def save_to_config(self, config_name, what_to_save, status):
        path = self.get_config_path(config_name)
        try:
            with open(path, 'r') as f:
                daten = json.load(f)
        except FileNotFoundError:
            daten = {}

        daten[what_to_save] = status

        with open(path, 'w') as f:
            json.dump(daten, f, indent=4)

    def load_from_config(self, config_name, name_in_config):
        path = self.get_config_path(config_name)
        with open(path, 'r') as f:
            daten = json.load(f)
        return daten[name_in_config]