#----------------------------------------------------------------------------------------------#
#----------------------------------- Made by Phönix -------------------------------------------#
#----------------------------------------------------------------------------------------------#
import json

class ConfigManager:
    def __init__(self):
        pass

    def clear_config(self, config_name):

        daten = {}

        with open(config_name, 'w') as f:
            json.dump(daten, f, indent=4)


    def save_to_config(self, config_name, what_to_save, status):
        try:
            with open(config_name, 'r') as f:
                daten = json.load(f)
        except FileNotFoundError:
            daten = {}

        daten[what_to_save] = status

        with open(config_name, 'w') as f:
            json.dump(daten, f, indent=4)

    def load_from_config(self, config_name, name_in_config):
        with open(config_name, 'r') as f:
            daten = json.load(f)

        load = daten[name_in_config]
        return load

    def create_and_save(self, data, config_name):
        daten = data

        with open(config_name, 'w') as f:
            json.dump(daten, f, indent=4)





