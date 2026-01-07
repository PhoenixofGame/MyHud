import json
import os
import customtkinter


class CrosshairManager:
    def __init__(self):
        self.entrys = {}
        self.tabviews = {}
        self.buttons = {}

        # Config-Einstellungen
        self.config_file = "crosshair_config.json"
        self.config = self.load_config()

        # Farben etc.
        self.set_main_color = "#1a1a1a"
        self.set_second_color = "#ffffff"
        self.set_accent_color = "#3498db"

    def load_config(self):
        """Lädt die Config-Datei beim Start"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Fehler beim Laden der Config. Erstelle neue...")
                return self.create_default_config()
        else:
            return self.create_default_config()

    def create_default_config(self):
        """Erstellt eine Standard-Config"""
        default_config = {
            "crosshair": {
                "farbe_entry_dot": "#FFFFFF",
                "outline_entry_dot": "#000000",
                "grose_entry_dot": 5.0
            },
            "window_settings": {
                "theme": "dark",
                "language": "de"
            }
        }
        self.save_config(default_config)
        return default_config

    def save_config(self, config_data=None):
        """Speichert die Config in die JSON-Datei"""
        if config_data is None:
            config_data = self.config

        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Fehler beim Speichern der Config: {e}")
            return False

    def get_config_value(self, section, key, default=None):
        """Holt einen Wert aus der Config"""
        try:
            return self.config.get(section, {}).get(key, default)
        except:
            return default

    def set_config_value(self, section, key, value):
        """Setzt einen Wert in der Config"""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value

    def create_entrys(self, window_name, set_tab, entry_name, placeholder_text, config_section="crosshair"):
        """Erstellt Entry-Felder mit Config-Unterstützung"""
        if window_name in self.tabviews:
            tab = self.tabviews[window_name].tab(set_tab)

        # Hole gespeicherten Wert aus Config
        saved_value = self.get_config_value(config_section, entry_name, "")

        entry = customtkinter.CTkEntry(
            tab,
            fg_color=self.set_main_color,
            text_color=self.set_second_color,
            placeholder_text=f"Set the Crosshair Color. (Current: {placeholder_text})"
        )
        entry.pack(fill="x", pady=8)

        # Setze gespeicherten Wert, falls vorhanden
        if saved_value:
            entry.insert(0, str(saved_value))

        self.entrys[entry_name] = entry
        return entry

    def save_cross_settings(self, window_name, set_tab, save_button=None, config_section="crosshair"):
        """Speichert alle Entry-Werte in die Config"""
        saved_values = {}

        for entry_name, entry_widget in self.entrys.items():
            value = entry_widget.get()

            if value != "":
                try:
                    # Versuche Float-Konvertierung für Größenangaben
                    if "grose" in entry_name.lower() or "size" in entry_name.lower():
                        saved_values[entry_name] = float(value)
                    else:
                        saved_values[entry_name] = value
                except ValueError:
                    saved_values[entry_name] = value

        # Aktualisiere Config
        if config_section not in self.config:
            self.config[config_section] = {}

        self.config[config_section].update(saved_values)

        # Speichere in Datei
        success = self.save_config()

        # Button Feedback
        if save_button and success:
            save_button.configure(text="✅ Saved!", fg_color="#00cc66")

            if window_name in self.tabviews:
                tab = self.tabviews[window_name].tab(set_tab)
                tab.after(1500, lambda: save_button.configure(
                    text="Save Settings", fg_color=self.set_accent_color
                ))
        elif save_button and not success:
            save_button.configure(text="❌ Error!", fg_color="#cc0000")
            if window_name in self.tabviews:
                tab = self.tabviews[window_name].tab(set_tab)
                tab.after(1500, lambda: save_button.configure(
                    text="Save Settings", fg_color=self.set_accent_color
                ))

        return saved_values

    def create_save_button(self, window_name, set_tab, config_section="crosshair"):
        """Erstellt den Save-Button"""
        if window_name in self.tabviews:
            tab = self.tabviews[window_name].tab(set_tab)

        save_button = customtkinter.CTkButton(
            tab,
            text="Save Settings",
            font=("Comic Sans MS", 25, "bold"),
            fg_color=self.set_accent_color,
            hover_color="#2980b9",
            text_color="black",
            command=lambda: self.save_cross_settings(window_name, set_tab, save_button, config_section)
        )
        save_button.pack(pady=20)

        self.buttons["save_button"] = save_button
        return save_button