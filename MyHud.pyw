import customtkinter
import os
import sys
import threading
import keyboard
import ctypes
import subprocess

from assets.Config_Manager import ConfigManager
from assets.UI_Class import UiClass
from assets.Settings_Class import SettingsMenu
from assets.gif_settings import GifSetting

from assets.crosshair import Crosshair
from assets.counter import Counter
from assets.text_display import Title_UI
from assets.main_overlay import Main_Overlay
from assets.keystrokes import Key_Overlay
from assets.gif_display import GifOverlay

VERSION = "v.2.0"

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

cm = ConfigManager()
cleanup_done = False

# ============ Cleanup-Funktion ============
def cleanup_and_exit():
    global cleanup_done, crosshair_process_save, title_process_save, gif_process_save, key_process_save, overlay_process_save, counter_process_save

    if cleanup_done:
        return
    cleanup_done = True

    if main.state() == "withdrawn":
        main.deiconify()
        main.attributes("-topmost", True)
        main.after(100, lambda: main.attributes("-topmost", False)) # noqa

    cm.save_to_config("assets/config.json", "crosshair_process_save",       status=crosshair_process_save)
    cm.save_to_config("assets/config.json", "title_process_save", status=title_process_save)
    cm.save_to_config("assets/config.json", "gif_process_save", status=gif_process_save)
    cm.save_to_config("assets/config.json", "key_process_save", status=key_process_save)
    cm.save_to_config("assets/config.json", "overlay_process_save", status=overlay_process_save)
    cm.save_to_config("assets/config.json", "counter_process_save", status=counter_process_save)

    main.focus_set()
    main.update()
    main.quit()
    sys.exit(0)

def restart_app():
    cm.save_to_config("assets/config.json", "crosshair_process_save",       status=crosshair_process_save)
    cm.save_to_config("assets/config.json", "title_process_save", status=title_process_save)
    cm.save_to_config("assets/config.json", "gif_process_save", status=gif_process_save)
    cm.save_to_config("assets/config.json", "key_process_save", status=key_process_save)
    cm.save_to_config("assets/config.json", "overlay_process_save", status=overlay_process_save)
    cm.save_to_config("assets/config.json", "counter_process_save", status=counter_process_save)

    if "__compiled__" in globals():
        exe = os.path.abspath(sys.argv[0])
        subprocess.Popen([exe], cwd=os.path.dirname(exe))
    else:
        subprocess.Popen([sys.executable] + sys.argv)
    os._exit(0)
# ======================================================
# ==================== LOAD ============================
# ======================================================
crosshair_process_save      = cm.load_from_config(config_name="assets/config.json", name_in_config="crosshair_process_save", default=False)
title_process_save          = cm.load_from_config(config_name="assets/config.json", name_in_config= "title_process_save", default=False)
gif_process_save            = cm.load_from_config(config_name="assets/config.json", name_in_config= "gif_process_save", default=False)
key_process_save            = cm.load_from_config(config_name="assets/config.json", name_in_config= "key_process_save", default=False)
overlay_process_save        = cm.load_from_config(config_name="assets/config.json", name_in_config= "overlay_process_save", default=False)
counter_process_save        = cm.load_from_config(config_name="assets/config.json", name_in_config= "counter_process_save", default=False)
color_preset                = cm.load_from_config(config_name="assets/config.json", name_in_config="color_preset", default="Cyberpunk")
design_font                 = cm.load_from_config(config_name="assets/config.json", name_in_config="design_font", default="Sitka")
fullscreen_toggle           = cm.load_from_config(config_name="assets/config.json", name_in_config="fullscreen", default="True")


# ======================================================
# =================== Farb presets =====================
# ======================================================
if color_preset == "Gloomy Nights":
    customtkinter.set_default_color_theme("assets/theme_assets/gloomy_nights_theme.json")

if color_preset == "Golden Hour":
    customtkinter.set_default_color_theme("assets/theme_assets/golden_hour_theme.json")

if color_preset == "Cyberpunk":
    customtkinter.set_default_color_theme("assets/theme_assets/cyberpunk_theme.json")

if color_preset == "Light Mode":
    customtkinter.set_default_color_theme("assets/theme_assets/light_mode_theme.json")

if color_preset == "Dark Mode":
    customtkinter.set_default_color_theme("assets/theme_assets/dark_mode_theme.json")

if color_preset == "Chocolate":
    customtkinter.set_default_color_theme("assets/theme_assets/chocolate_theme.json")

if color_preset == "Old School":
    customtkinter.set_default_color_theme("assets/theme_assets/old_school_theme.json")

if color_preset == "Deep Sea":
    customtkinter.set_default_color_theme("assets/theme_assets/deep_sea_theme.json")

TEXT_FONT = design_font

ctypes.windll.shcore.SetProcessDpiAwareness(2) # noqa

# ======================================================
# =================== Hauptfenster =====================
# ======================================================
main = customtkinter.CTk()
main.title("Phönix´s Hud")

scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100  # noqa
customtkinter.set_widget_scaling(1.0 / scale_factor)
customtkinter.set_window_scaling(1.0 / scale_factor)

main.update_idletasks()

if fullscreen_toggle == "True":
    main.overrideredirect(True)
    screen_width = main.winfo_screenwidth()
    screen_height = main.winfo_screenheight()

if fullscreen_toggle == "False":
    main.overrideredirect(False)
    screen_width = 1150
    screen_height = 750

main.resizable(False, False)
main.attributes("-transparentcolor", "#100001")  # noqa
main.wm_attributes("-alpha", 0.95)
main.attributes("-topmost", True)


main.geometry(f"{screen_width}x{screen_height}+0+0")

main.update_idletasks()

screen_x = screen_width/2
screen_y = (screen_height/2)
tab_width = int(screen_width * 0.75)
tab_height = int(screen_height * 0.85)

main.protocol("WM_DELETE_WINDOW", cleanup_and_exit)
main.iconbitmap("assets/icon.ico")

custom_font = customtkinter.CTkFont(family=TEXT_FONT, size=20, weight="bold")
titel = customtkinter.CTkLabel(
    main,
    text=f"My Hud {VERSION}",
    font=custom_font,
    width=200,
    height=30
)
titel.place(x=5, y=5)

# ======================================================
# ==================== Tabs ============================
# ======================================================
# Tabview
tabview = customtkinter.CTkTabview(
    main,
    width=screen_width - 50,
    height=screen_height - 50
)
tabview.place(x=screen_width//2, y=(screen_height/2) +10, anchor="center")

# tabs
tabview.add("✨ UI Improvements")
tabview.add("▶️ Gif Display")
tabview.add("⚙️ Settings")

# frames
ui_improvement_frame = customtkinter.CTkScrollableFrame(tabview.tab("✨ UI Improvements"), fg_color="transparent", corner_radius=20)
ui_improvement_frame.pack(expand=True, fill="both", padx=20, pady=20)

gif_frame = customtkinter.CTkScrollableFrame(tabview.tab("▶️ Gif Display"), fg_color="transparent", corner_radius=20)
gif_frame.pack(expand=True, fill="both", padx=20, pady=20)

setting_frame = customtkinter.CTkScrollableFrame(tabview.tab("⚙️ Settings"), fg_color="transparent", corner_radius=20)
setting_frame.pack(expand=True, fill="both", padx=20, pady=20)

tabview._segmented_button.configure(font=custom_font) # noqa
# ======================================================
# ================== Switches ==========================
# ======================================================
crosshair_process = None
titel_process = None
gif_process = None
key_process = None
overlay_process = None
counter_process = None

counter_thread = None
keystrokes_thread = None
gif_thread = None

def CrosshairSwitch():
    global crosshair_process, crosshair_process_save
    if Crosshair_UI.main_button.get():
        crosshair_process = Crosshair(config_file="assets/crosshair_config.json", master=main)
        crosshair_process.start_crosshair()

        crosshair_process_save = True
    else:
        if crosshair_process is not None:
            crosshair_process.stop_crosshair()
            crosshair_process = None

        crosshair_process_save = False

def TitelSwitch():
    global titel_process, title_process_save
    if Titel_anzeige.main_button.get():
        titel_process = Title_UI(config_file="assets/config.json", master=main)
        titel_process.start_title()

        title_process_save = True
    else:
        if titel_process is not None:
            titel_process.stop_title()

        titel_process = None
        title_process_save = False

def GifSwitch():
    global gif_process, gif_process_save, gif_thread
    if Gif_anzeige.main_button.get():
        gif_process = GifOverlay(config_file="assets/gif_config.json", master=main)
        gif_process.start_gif()

        gif_process_save = True
    else:
        if gif_process is not None:
            gif_process.stop_gif()

        gif_process = None
        gif_process_save = False

def KeySwitch():
    global key_process, key_process_save, keystrokes_thread
    if Key_anzeige.main_button.get():
        key_process = Key_Overlay(config_file="assets/config.json", master=main)
        keystrokes_thread = threading.Thread(target=key_process.start_key_overlay, daemon=True)
        keystrokes_thread.start()

        key_process_save = True
    else:
        if key_process is not None:
            key_process.stop_key_overlay()

        key_process = None
        key_process_save = False

def UiSwitch():
    global overlay_process, overlay_process_save
    if Main_UI.main_button.get():
        overlay_process = Main_Overlay(config_file="assets/config.json", master=main)
        overlay_process.start_main_overlay()

        overlay_process_save = True
    else:
        if overlay_process is not None:
            overlay_process.stop_main_overlay()

        overlay_process = None
        overlay_process_save = False

def CounterSwitch():
    global counter_process, counter_process_save, counter_thread
    if Counter_UI.main_button.get():
        counter_process = Counter(config_file="assets/config.json", master=main)
        counter_thread = threading.Thread(target=counter_process.start_counter, daemon=True)
        counter_thread.start()

        counter_process_save = True
    else:
        if counter_process is not None:
            counter_process.stop_counter()

        counter_process = None
        counter_process_save = False
# ======================================================
# =================  Settings  =========================
# ======================================================
class SettingsToggle:
    def __init__(self, name, font, config_file, restart_func, menu_class=SettingsMenu):
        self.menu = menu_class(name, font, config_file)
        self.restart_func = restart_func
        self.is_open = False

    def toggle(self, master, setup_func):
        if self.is_open:
            self.menu.destroy(master)
            self.menu.entries = []
            self.is_open = False
        else:
            self.menu.create_new(master, restart_func=self.restart_func)
            setup_func(self.menu)
            self.is_open = True

class CrosshairToggle:
    def __init__(self):
        self.frame = None
        self.is_open = False

    def toggle(self, master, setup_func, **frame_kwargs):
        if self.is_open and self.frame is not None:
            self.frame.destroy()
            self.frame = None
            self.is_open = False
        else:
            self.frame = customtkinter.CTkFrame(master, **frame_kwargs)
            self.frame.pack()
            setup_func(self.frame)
            self.is_open = True

def crosshair_restart():
    global crosshair_process
    if crosshair_process is not None:
        crosshair_process.stop_crosshair()

        def recreate():
            global crosshair_process
            crosshair_process = Crosshair(config_file="assets/crosshair_config.json", master=main)
            crosshair_process.start_crosshair()

        main.after(50, recreate)

def title_restart():
    global titel_process
    if titel_process is not None:
        titel_process.stop_title()

        def recreate():
            global titel_process
            titel_process = Title_UI(config_file="assets/config.json", master=main)
            titel_process.start_title()

        main.after(50, recreate)

def key_restart():
    global key_process, keystrokes_thread
    if key_process is not None:
        key_process.stop_key_overlay()
        if keystrokes_thread is not None:
            keystrokes_thread.join(timeout=2)

    key_process = Key_Overlay(config_file="assets/config.json", master=main)
    keystrokes_thread = threading.Thread(target=key_process.start_key_overlay, daemon=True)
    keystrokes_thread.start()

def main_ui_restart():
    global overlay_process
    if overlay_process is not None:
        overlay_process.stop_main_overlay()

        def recreate():
            global overlay_process
            overlay_process = Main_Overlay(config_file="assets/config.json", master=main)
            overlay_process.start_main_overlay()
        main.after(50, recreate)

def counter_restart():
    global counter_process, counter_thread
    if counter_process is not None:
        counter_process.stop_counter()
        if counter_thread is not None:
            counter_thread.join(timeout=2)

    counter_process = Counter(config_file="assets/config.json", master=main)
    counter_thread = threading.Thread(target=counter_process.start_counter, daemon=True)
    counter_thread.start()

def gif_restart():
    global gif_process
    if gif_process is not None:
        gif_process.stop_gif()

        def recreate():
            global gif_process
            gif_process = GifOverlay(config_file="assets/gif_config.json", master=main,
                                     on_drop=gif_toggle.menu.update_position)
            gif_process.start_gif()

        main.after(50, recreate)
    else:
        gif_process = GifOverlay(config_file="assets/gif_config.json", master=main,
                                 on_drop=gif_toggle.menu.update_position)
        gif_process.start_gif()

def restart_if_design_changed():
    new_preset = cm.load_from_config("assets/config.json", "color_preset", "Cyberpunk")
    new_font = cm.load_from_config("assets/config.json", "design_font", "Sitka")
    new_fullscreen = cm.load_from_config(config_name="assets/config.json", name_in_config="fullscreen", default="True")

    if new_preset != color_preset or new_font != design_font or new_fullscreen != fullscreen_toggle:
        restart_app()

Title_Settings_Toggle     = SettingsToggle("Title", TEXT_FONT, "assets/config.json", restart_func= title_restart)
Key_Settings_Toggle       = SettingsToggle("Keys", TEXT_FONT, "assets/config.json", restart_func= key_restart)
Main_Ui_Settings_Toggle   = SettingsToggle("Main UI", TEXT_FONT, "assets/config.json", restart_func= main_ui_restart)
Counter_Settings_Toggle   = SettingsToggle("Counter", TEXT_FONT, "assets/config.json", restart_func= counter_restart)
gif_toggle                = SettingsToggle("Gif", TEXT_FONT, "assets/gif_config.json", restart_func= gif_restart, menu_class=GifSetting)
design_color_toggle       = SettingsToggle("Design", TEXT_FONT, "assets/config.json", restart_func=restart_if_design_changed)

crosshair_toggle    = CrosshairToggle()

def CrosshairSettings():
    def total_setup(frame):
        dot_toggle      = SettingsToggle("DoT",       TEXT_FONT, "assets/crosshair_config.json", restart_func=crosshair_restart)
        square_toggle   = SettingsToggle("Square",    TEXT_FONT, "assets/crosshair_config.json", restart_func=crosshair_restart)
        x_toggle        = SettingsToggle("X",         TEXT_FONT, "assets/crosshair_config.json", restart_func=crosshair_restart)
        plus_toggle     = SettingsToggle("Plus",      TEXT_FONT, "assets/crosshair_config.json", restart_func=crosshair_restart)
        trie_toggle     = SettingsToggle("Triangle",  TEXT_FONT, "assets/crosshair_config.json", restart_func=crosshair_restart)

        def crosshair_dot_settings():
            def setup(menu):
                dot_color = cm.load_from_config("assets/crosshair_config.json", "dot_color","#000001")
                dot_outline = cm.load_from_config("assets/crosshair_config.json", "dot_outline","rgb")
                dot_size = cm.load_from_config("assets/crosshair_config.json", "dot_size",120.0)
                menu.add_color_picker(text="Set the Crosshair Color: ", default_color=dot_color, save_variable="dot_color")
                menu.add_color_picker(text="Set the Outline Color: ", default_color=dot_outline, save_variable="dot_outline")
                menu.add_entry("dot_size", text= "Set the Crosshair Size: ", placeholder= f"(Current: {dot_size})" , value_type=float)

            dot_toggle.toggle(frame, setup)

        def crosshair_dot_main():
            dot_activation = cm.load_from_config("assets/crosshair_config.json", "dot_activation", False)
            dot_activation = not dot_activation
            cm.save_to_config("assets/crosshair_config.json", "dot_activation", dot_activation)
            crosshair_restart()

        def crosshair_square_settings():
            def setup(menu):
                rectangle_color = cm.load_from_config("assets/crosshair_config.json", "rectangle_color","rgb")
                rectangle_outline = cm.load_from_config("assets/crosshair_config.json", "rectangle_outline", "black")
                rectangle_size = cm.load_from_config("assets/crosshair_config.json", "rectangle_size", 2.5)
                menu.add_color_picker(text="Set the Crosshair Color: ", default_color=rectangle_color, save_variable="rectangle_color")
                menu.add_color_picker(text="Set the Outline Color: ", default_color=rectangle_outline, save_variable="rectangle_outline")
                menu.add_entry("rectangle_size", text= "Set the Crosshair Size: " , placeholder=f"(Current: {rectangle_size})", value_type=float)

            square_toggle.toggle(frame, setup)

        def crosshair_square_main():
            rectangle_activation = cm.load_from_config("assets/crosshair_config.json", "rectangle_activation", False)
            rectangle_activation = not rectangle_activation
            cm.save_to_config("assets/crosshair_config.json", "rectangle_activation", rectangle_activation)
            crosshair_restart()

        def crosshair_x_settings():
            def setup(menu):
                x_color = cm.load_from_config("assets/crosshair_config.json", "x_color", "white")
                x_size = cm.load_from_config("assets/crosshair_config.json", "x_size", 50.0)
                x_gap = cm.load_from_config("assets/crosshair_config.json", "x_gap", 10.0)
                x_width = cm.load_from_config("assets/crosshair_config.json", "x_width", 2.0)
                menu.add_color_picker(text="Set the Crosshair Color: ", default_color=x_color, save_variable="x_color")
                menu.add_entry("x_size", text= "Set the Crosshair Size: ", placeholder= f"(Current: {x_size})", value_type=float)
                menu.add_entry("x_gap", text= "Set the Crosshair Gap: ", placeholder= f"(Current: {x_gap})", value_type=float)
                menu.add_entry("x_width", text="Set the Crosshair Width: ", placeholder= f"(Current: {x_width})", value_type=float)

            x_toggle.toggle(frame, setup)

        def crosshair_x_main():
            x_activation = cm.load_from_config("assets/crosshair_config.json", "x_activation", False)
            x_activation = not x_activation
            cm.save_to_config("assets/crosshair_config.json", "x_activation", x_activation)
            crosshair_restart()

        def crosshair_plus_settings():
            def setup(menu):
                plus_color = cm.load_from_config("assets/crosshair_config.json", "plus_color", "#03fcba")
                plus_size = cm.load_from_config("assets/crosshair_config.json", "plus_size", 5.0)
                plus_gap = cm.load_from_config("assets/crosshair_config.json", "plus_gap", 1.0)
                plus_width = cm.load_from_config("assets/crosshair_config.json", "plus_width", 2.0)
                menu.add_color_picker(text="Set the Crosshair Color: ", default_color=plus_color, save_variable="plus_color")
                menu.add_entry("plus_size", text= f"Set the Crosshair Size: ", placeholder= f"(Current: {plus_size})", value_type=float)
                menu.add_entry("plus_gap", text= "Set the Crosshair Gap: ", placeholder= f"(Current: {plus_gap})",value_type=float)
                menu.add_entry("plus_width", text="Set the Crosshair Width: ", placeholder= f"(Current: {plus_width})", value_type=float)

            plus_toggle.toggle(frame, setup)

        def crosshair_plus_main():
            plus_activation = cm.load_from_config("assets/crosshair_config.json", "plus_activation", True)
            plus_activation = not plus_activation
            cm.save_to_config("assets/crosshair_config.json", "plus_activation", plus_activation)
            crosshair_restart()

        def crosshair_trie_settings():
            def setup(menu):
                triangle_color = cm.load_from_config("assets/crosshair_config.json", "triangle_color", "#a0a0a0")
                triangle_size = cm.load_from_config("assets/crosshair_config.json", "triangle_size", 60.0)
                triangle_width = cm.load_from_config("assets/crosshair_config.json", "triangle_width", 10.0)
                menu.add_color_picker(text="Set the Crosshair Color: ", default_color=triangle_color, save_variable="triangle_color")
                menu.add_entry("triangle_size", text= "Set the Crosshair Size: ", placeholder= f"(Current: {triangle_size})", value_type=float)
                menu.add_entry("triangle_width", text="Set the Crosshair Width: ", placeholder= f"(Current: {triangle_width})", value_type=float)

            trie_toggle.toggle(frame, setup)

        def crosshair_trie_main():
            triangle_activation = cm.load_from_config("assets/crosshair_config.json", "triangle_activation", False)
            triangle_activation = not triangle_activation
            cm.save_to_config("assets/crosshair_config.json", "triangle_activation", triangle_activation)
            crosshair_restart()

        def close_all_toggles():
            for toggle in [dot_toggle, square_toggle, x_toggle, plus_toggle, trie_toggle]:
                if toggle.is_open:
                    toggle.menu.destroy(frame)
                    toggle.menu.entries = []
                    toggle.is_open = False

        tabview_settings = customtkinter.CTkTabview(frame, width=1230, height=100, command=close_all_toggles)
        tabview_settings.pack(expand=True, fill="both", padx=20, pady=20)

        # tabs adden
        tabview_settings.add("Dot")
        tabview_settings.add("Square")
        tabview_settings.add("X")
        tabview_settings.add("Plus")
        tabview_settings.add("Triangle")

        custom_font_settings = customtkinter.CTkFont(family=TEXT_FONT, size=30, weight="bold")  # ändert Schriftgröße und Farbe der Taps
        tabview_settings._segmented_button.configure(font=custom_font_settings)  # noqa

        crosshair_dot = UiClass("Dot", font=TEXT_FONT)
        crosshair_dot.create_module(tabview_settings.tab("Dot"), crosshair_dot_main, crosshair_dot_settings, "Toggle Dot")
        crosshair_square = UiClass("Square", font=TEXT_FONT)
        crosshair_square.create_module(tabview_settings.tab("Square"), crosshair_square_main, crosshair_square_settings, "Toggle Square")
        crosshair_x = UiClass("X", font=TEXT_FONT)
        crosshair_x.create_module(tabview_settings.tab("X"), crosshair_x_main, crosshair_x_settings, "Toggle X")
        crosshair_plus = UiClass("Plus", font=TEXT_FONT)
        crosshair_plus.create_module(tabview_settings.tab("Plus"), crosshair_plus_main, crosshair_plus_settings, "Toggle Plus")
        crosshair_trie = UiClass("Triangle", font=TEXT_FONT)
        crosshair_trie.create_module(tabview_settings.tab("Triangle"), crosshair_trie_main, crosshair_trie_settings, "Toggle Triangle")

        # autostart und so
        dot_is_active = cm.load_from_config(config_name="assets/crosshair_config.json", name_in_config="dot_activation", default=False) == True
        if dot_is_active:
            crosshair_dot.main_button.select()
        square_is_active = cm.load_from_config(config_name="assets/crosshair_config.json", name_in_config="rectangle_activation", default=False) == True
        if square_is_active:
            crosshair_square.main_button.select()
        x_is_active = cm.load_from_config(config_name="assets/crosshair_config.json", name_in_config="x_activation", default=False) == True
        if x_is_active:
            crosshair_x.main_button.select()
        plus_is_active = cm.load_from_config(config_name="assets/crosshair_config.json", name_in_config="plus_activation", default=True) == True
        if plus_is_active:
            crosshair_plus.main_button.select()
        trie_is_active = cm.load_from_config(config_name="assets/crosshair_config.json", name_in_config="triangle_activation", default=False) == True
        if trie_is_active:
            crosshair_trie.main_button.select()

    crosshair_toggle.toggle(ui_improvement_frame, total_setup, corner_radius=20)

def TitleSettings():
    def setup(menu):
        title_default_text = cm.load_from_config(config_name="assets/config.json", name_in_config="title_default_text", default="WWW")
        title_color = cm.load_from_config(config_name="assets/config.json", name_in_config="title_color", default="red")
        title_size = cm.load_from_config(config_name="assets/config.json", name_in_config="title_size", default=20)

        menu.add_entry("title_default_text", f"Set the Title text. ", placeholder=f"(Current: {title_default_text})")
        menu.add_entry("title_size", f"Set the Title size. ", placeholder=f"(Current: {title_size})", value_type=int)
        menu.add_color_picker(text="Set the Title color. ", default_color=title_color, save_variable="title_color")

    Title_Settings_Toggle.toggle(ui_improvement_frame, setup)

def GifSettings():
    gif_toggle.toggle(gif_frame, lambda menu: None)

def KeySettings():
    def setup(menu):
        key_default_color = cm.load_from_config(config_name="assets/config.json", name_in_config="key_default_color", default="black")
        key_color_pressed = cm.load_from_config(config_name="assets/config.json", name_in_config="key_color_pressed", default="white")
        key_x_location = cm.load_from_config(config_name="assets/config.json", name_in_config="key_x_location", default=1740)
        key_y_location = cm.load_from_config(config_name="assets/config.json", name_in_config="key_y_location", default=80.0)
        key_text_font = cm.load_from_config(config_name="assets/config.json", name_in_config="key_text_font", default="Comic Sans MS")
        key_text_size = cm.load_from_config(config_name="assets/config.json", name_in_config="key_text_size", default=15)
        key_outline_color = cm.load_from_config(config_name="assets/config.json", name_in_config="key_outline_color", default="black")
        key_text_color = cm.load_from_config(config_name="assets/config.json", name_in_config="key_text_color", default="#03fcba")

        menu.add_color_picker(text="Set the default Color. ", default_color=key_default_color, save_variable="key_default_color", show_rgb=False)
        menu.add_color_picker(text="Set the pressed Color. ", default_color=key_color_pressed, save_variable="key_color_pressed", show_rgb=False)
        menu.add_color_picker(text="Set the Outline Color. ", default_color=key_outline_color, save_variable="key_outline_color", show_rgb=False)
        menu.add_color_picker(text="Set the Text Color. ", default_color=key_text_color, save_variable="key_text_color", show_rgb=False)
        menu.add_entry("key_x_location", f"Set the X Location. ", placeholder= f"(Current: {key_x_location})", value_type=int)
        menu.add_entry("key_y_location", f"Set the Y Location. ", placeholder= f"(Current: {key_y_location})", value_type=int)
        menu.add_entry("key_text_font", f"Set the Key Font. ", placeholder= f"(Current: {key_text_font})")
        menu.add_entry("key_text_size", f"Set the Font Size. ", placeholder= f"(Current: {key_text_size})", value_type=int)

    Key_Settings_Toggle.toggle(ui_improvement_frame, setup)

def UiSettings():
    def setup(menu):
        main_overlay_motivation_color = cm.load_from_config(config_name="assets/config.json", name_in_config="main_overlay_motivation_color", default="rgb")
        main_overlay_motivation_size = cm.load_from_config(config_name="assets/config.json", name_in_config="main_overlay_motivation_size", default=15)
        main_overlay_clock_color = cm.load_from_config(config_name="assets/config.json", name_in_config="main_overlay_clock_color", default="#ffffff")
        main_overlay_clock_size = cm.load_from_config(config_name="assets/config.json", name_in_config="main_overlay_clock_size", default=15)
        main_overlay_spotify_color = cm.load_from_config(config_name="assets/config.json", name_in_config="main_overlay_spotify_color", default="white")
        main_overlay_spotify_size = cm.load_from_config(config_name="assets/config.json", name_in_config="main_overlay_spotify_size", default=15)

        menu.add_color_picker(text="Set the Motivation Text Color. ", default_color=main_overlay_motivation_color, save_variable="main_overlay_motivation_color", show_rgb=True)
        menu.add_entry("main_overlay_motivation_size", f"Set the Motivation Text Size. ", placeholder= f"(Current: {main_overlay_motivation_size})", value_type=int)
        menu.add_color_picker(text="Set the Clock Color. ", default_color=main_overlay_clock_color, save_variable="main_overlay_clock_color", show_rgb=True)
        menu.add_entry("main_overlay_clock_size", f"Set the Clock Size. ", placeholder= f"(Current: {main_overlay_clock_size})", value_type=int)
        menu.add_color_picker(text="Set the Spotify Color. ", default_color=main_overlay_spotify_color, save_variable="main_overlay_spotify_color", show_rgb=True)
        menu.add_entry("main_overlay_spotify_size", f"Set the Spotify Size. ", placeholder= f"(Current: {main_overlay_spotify_size})", value_type=int)

    Main_Ui_Settings_Toggle.toggle(ui_improvement_frame, setup)

def CounterSettings():
    def setup(menu):
        counter_text = cm.load_from_config(config_name="assets/config.json", name_in_config="counter_text", default="Default Text")
        counter_font = cm.load_from_config(config_name="assets/config.json", name_in_config="counter_font", default="Sitka")
        counter_size = cm.load_from_config(config_name="assets/config.json", name_in_config="counter_size", default=50)
        counter_color = cm.load_from_config(config_name="assets/config.json", name_in_config="counter_color", default="#690f96")
        counter_default_value = cm.load_from_config(config_name="assets/config.json", name_in_config="counter_default_value", default=0)
        counter_hotkey_positive = cm.load_from_config(config_name="assets/config.json", name_in_config="counter_hotkey_positive", default="r")
        counter_hotkey_negative = cm.load_from_config(config_name="assets/config.json", name_in_config="counter_hotkey_negative", default="T")
        counter_x_location = cm.load_from_config(config_name="assets/config.json", name_in_config="counter_x_location", default=500)
        counter_y_location = cm.load_from_config(config_name="assets/config.json", name_in_config="counter_y_location", default=100)

        menu.add_entry("counter_text", f"Set the Counter Text. ", placeholder= f"(Current: {counter_text})")
        menu.add_entry("counter_font", f"Set the Counter Font. ", placeholder=f"(Current: {counter_font})")
        menu.add_entry("counter_size", f"Set the Counter Size. ", placeholder=f"(Current: {counter_size})", value_type=int)
        menu.add_entry("counter_default_value", f"Set the Counter Value. ", placeholder=f"(Current: {counter_default_value})", value_type=int)
        menu.add_entry("counter_hotkey_positive", f"Set the Counter Add Hotkey. ", placeholder=f"(Current: {counter_hotkey_positive})")
        menu.add_entry("counter_hotkey_negative", f"Set the Counter Subtract Hotkey. ", placeholder=f"(Current: {counter_hotkey_negative})")
        menu.add_entry("counter_x_location", f"Set the Counter X Location. ", placeholder=f"(Current: {counter_x_location})", value_type=int)
        menu.add_entry("counter_y_location", f"Set the Counter Y Location. ", placeholder=f"(Current: {counter_y_location})", value_type=int)
        menu.add_color_picker(text="Set the Counter Color. ", default_color=counter_color, save_variable="counter_color", show_rgb=True)

    Counter_Settings_Toggle.toggle(ui_improvement_frame, setup)

def design_color_settings():
    def setup(menu):
        design_color = cm.load_from_config("assets/config.json", "color_preset", "Cyberpunk")
        design_font = cm.load_from_config("assets/config.json", "design_font", "Sitka")
        fullscreen = cm.load_from_config("assets/config.json", "fullscreen", "True")

        menu.add_dropdown("color_preset", "Set the Design Preset.", options=["Cyberpunk", "Golden Hour", "Gloomy Nights", "Light Mode", "Dark Mode", "Chocolate", "Old School", "Deep Sea"], saved_value=design_color)
        menu.add_entry("design_font", "Set the Client Font.", placeholder=f"(Current: {design_font})")
        menu.add_switch(switch_text="Toggle Fullscreen.", save_stuff="fullscreen", saved_status=fullscreen)

    design_color_toggle.toggle(setting_frame, setup)
# ======================================================
# ====================  UI  ============================
# ======================================================
# ui stuf
Crosshair_UI = UiClass("Crosshair_UI", font=TEXT_FONT)
Crosshair_UI.create_module(ui_improvement_frame, CrosshairSwitch, CrosshairSettings, label_text="🎯 Crosshair")

Titel_anzeige = UiClass("Titel_anzeige", font=TEXT_FONT)
Titel_anzeige.create_module(ui_improvement_frame, TitelSwitch, TitleSettings, label_text="🗒 Display A Text")

Key_anzeige = UiClass("Key_anzeige", font=TEXT_FONT)
Key_anzeige.create_module(ui_improvement_frame, KeySwitch, KeySettings, label_text="🎮 Key Overlay")

Main_UI = UiClass("Main_UI", font=TEXT_FONT)
Main_UI.create_module(ui_improvement_frame, UiSwitch, UiSettings, label_text="🖼 Main Overlay")

Counter_UI = UiClass("Counter_UI", font=TEXT_FONT)
Counter_UI.create_module(ui_improvement_frame, CounterSwitch, CounterSettings, label_text="🎰 Counter")

# Gif stuff
Gif_anzeige = UiClass("Gif_anzeige", font=TEXT_FONT)
Gif_anzeige.create_module(gif_frame, GifSwitch, GifSettings, label_text="🎞 Display A GIF")

# Settings stuff
design_color_UI = UiClass("Client_Style", font=TEXT_FONT)
design_color_UI.create_module(setting_frame, None, design_color_settings,"Client Style")

# ======================================================
# ===================  Auto  ===========================
# ======================================================
if crosshair_process_save:
    Crosshair_UI.main_button.select()
    CrosshairSwitch()

if title_process_save:
    Titel_anzeige.main_button.select()
    TitelSwitch()

if gif_process_save:
    Gif_anzeige.main_button.select()
    GifSwitch()

if key_process_save:
    Key_anzeige.main_button.select()
    KeySwitch()

if overlay_process_save:
    Main_UI.main_button.select()
    UiSwitch()

if counter_process_save:
    Counter_UI.main_button.select()
    CounterSwitch()

# ======================================================
# ===================  toggle  =========================
# ======================================================
def toggle_window():
    if main.state() == "withdrawn":
        main.deiconify()
        main.attributes("-topmost", True)
        main.after(100, lambda: main.attributes("-topmost", False)) # noqa
    else:
        main.withdraw()

keyboard.add_hotkey("right shift", toggle_window)
keyboard.add_hotkey("f3", lambda: threading.Thread(target=cleanup_and_exit, daemon=True).start())

if __name__ == "__main__":
    try:
        main.mainloop()
    finally:
        cleanup_and_exit()