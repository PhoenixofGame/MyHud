import customtkinter
import subprocess
import os
import sys
import keyboard
from assets.ConfigManager import ConfigManager
from assets.UI_Class import UiClass
from assets.Settings_Class import SettingsMenu
from assets.gif_settings import GifSetting

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

# ============ Farben & Themes ============
BG_COLOR = "black"
MAIN_COLOR = "grey"
TEXT_COLOR = "white"
ACCENT_COLOR = "#cfcccc"
ACCENT_HOVER = "white"
INVIS_COLOR = "#000001"


# ============ Cleanup-Funktion ============
def cleanup_and_exit():
    global crosshair_process, crosshair_process_save, titel_process, title_process_save, gif_process, gif_process_save,key_process, key_process_save, overlay_process, overlay_process_save, counter_process, counter_process_save

    # Alle Subprozesse beenden
    for process in [crosshair_process, titel_process, gif_process,key_process, overlay_process, counter_process]:
        if process and hasattr(process, 'poll') and process.poll() is None:
            process.terminate()
            process.wait(timeout=2)

    ConfigManager().save_to_config("assets/config.json", "crosshair_process_save", status=crosshair_process_save)
    ConfigManager().save_to_config("assets/config.json", "title_process_save", status=title_process_save)
    ConfigManager().save_to_config("assets/config.json", "gif_process_save", status=gif_process_save)
    ConfigManager().save_to_config("assets/config.json", "key_process_save", status=key_process_save)
    ConfigManager().save_to_config("assets/config.json", "overlay_process_save", status=overlay_process_save)
    ConfigManager().save_to_config("assets/config.json", "counter_process_save", status=counter_process_save)

    main.quit()
    main.destroy()

    sys.exit(0)

# ======================================================
# ==================== LOAD ============================
# ======================================================
try:
    crosshair_process_save = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config="crosshair_process_save")
    title_process_save = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config= "title_process_save")
    gif_process_save = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config= "gif_process_save")
    key_process_save = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config= "key_process_save")
    overlay_process_save = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config= "overlay_process_save")
    counter_process_save = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config= "counter_process_save")
except FileNotFoundError:
    print("main config error!")
    crosshair_process_save = False
    title_process_save = False
    gif_process_save = False
    key_process_save = False
    overlay_process_save = False
    counter_process_save = False

customtkinter.set_appearance_mode("dark")

# ============ Hauptfenster ============
main = customtkinter.CTk()
main.title("Phönix´s Hud")
main.geometry("800x620")
main.resizable(False, False)
main.attributes("-transparentcolor", INVIS_COLOR)  # noqa
main.configure(fg_color=BG_COLOR)
main.wm_attributes("-alpha", 0.95)
main.protocol("WM_DELETE_WINDOW", cleanup_and_exit)
main.iconbitmap("assets/icon.ico")
main.grid_columnconfigure(0, weight=1)

# Titel darüber
titel = customtkinter.CTkLabel(
    main,
    text=" -- My Hud --",
    font=("Comic Sans MS", 55, "bold"),
    text_color="white",
    fg_color="transparent",
    bg_color="transparent"
)
titel.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

# scroll holder

holder = customtkinter.CTkScrollableFrame(main, height=490, fg_color="transparent", scrollbar_button_color = "grey", scrollbar_button_hover_color = "#b5b4b1")
holder.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

# ======================================================
# ==================== DEVS ============================
# ======================================================
def CrosshairSwitch():
    global crosshair_process, crosshair_process_save
    if Crosshair.main_button.get():
        crosshair_process = subprocess.Popen(["pythonw", os.path.join("assets", "crosshair.pyw")])
        crosshair_process_save = True
    else:
        crosshair_process.terminate()
        crosshair_process = None
        crosshair_process_save = False

def CrosshairSettings():
    def crosshair_dot_settings():
        dot_color = ConfigManager().load_from_config("assets/crosshair_config.json", "dot_color")
        dot_outline = ConfigManager().load_from_config("assets/crosshair_config.json", "dot_outline")
        dot_size = ConfigManager().load_from_config("assets/crosshair_config.json", "dot_size")
        crosshair_settings = SettingsMenu("DoT", main_color=MAIN_COLOR, secondary_color=ACCENT_COLOR,hover_color=ACCENT_HOVER, config_file="assets/crosshair_config.json")
        crosshair_settings.create_new(crosshair_menu, 1)
        crosshair_settings.add_color_picker(text="Set the Crosshair Color: ", default_color=dot_color, save_variable="dot_color")
        crosshair_settings.add_color_picker(text="Set the Outline Color: ", default_color=dot_outline, save_variable="dot_outline")
        crosshair_settings.add_entry("dot_size", text= "Set the Crosshair Size: ", placeholder= f"(Current: {dot_size})" , value_type=float)

    def crosshair_dot_main():
        dot_activation = ConfigManager().load_from_config("assets/crosshair_config.json", "dot_activation")
        dot_activation = not dot_activation
        ConfigManager().save_to_config("assets/crosshair_config.json", "dot_activation", dot_activation)

    def crosshair_square_settings():
        rectangle_color = ConfigManager().load_from_config("assets/crosshair_config.json", "rectangle_color")
        rectangle_outline = ConfigManager().load_from_config("assets/crosshair_config.json", "rectangle_outline")
        rectangle_size = ConfigManager().load_from_config("assets/crosshair_config.json", "rectangle_size")
        crosshair_settings = SettingsMenu("Square", main_color=MAIN_COLOR, secondary_color=ACCENT_COLOR,hover_color=ACCENT_HOVER, config_file="assets/crosshair_config.json")
        crosshair_settings.create_new(crosshair_menu,1)
        crosshair_settings.add_color_picker(text="Set the Crosshair Color: ", default_color=rectangle_color, save_variable="rectangle_color")
        crosshair_settings.add_color_picker(text="Set the Outline Color: ", default_color=rectangle_outline, save_variable="rectangle_outline")
        crosshair_settings.add_entry("rectangle_size", text= "Set the Crosshair Size: " , placeholder=f"(Current: {rectangle_size})", value_type=float)

    def crosshair_square_main():
        rectangle_activation = ConfigManager().load_from_config("assets/crosshair_config.json", "rectangle_activation")
        rectangle_activation = not rectangle_activation
        ConfigManager().save_to_config("assets/crosshair_config.json", "rectangle_activation", rectangle_activation)

    def crosshair_x_settings():
        x_color = ConfigManager().load_from_config("assets/crosshair_config.json", "x_color")
        x_size = ConfigManager().load_from_config("assets/crosshair_config.json", "x_size")
        x_gap = ConfigManager().load_from_config("assets/crosshair_config.json", "x_gap")
        x_width = ConfigManager().load_from_config("assets/crosshair_config.json", "x_width")
        crosshair_settings = SettingsMenu("X", main_color=MAIN_COLOR, secondary_color=ACCENT_COLOR,hover_color=ACCENT_HOVER, config_file="assets/crosshair_config.json")
        crosshair_settings.create_new(crosshair_menu,1)
        crosshair_settings.add_color_picker(text="Set the Crosshair Color: ", default_color=x_color, save_variable="x_color")
        crosshair_settings.add_entry("x_size", text= "Set the Crosshair Size: ", placeholder= f"(Current: {x_size})", value_type=float)
        crosshair_settings.add_entry("x_gap", text= "Set the Crosshair Gap: ", placeholder= f"(Current: {x_gap})", value_type=float)
        crosshair_settings.add_entry("x_width", text="Set the Crosshair Width: ", placeholder= f"(Current: {x_width})", value_type=float)
    def crosshair_x_main():
        x_activation = ConfigManager().load_from_config("assets/crosshair_config.json", "x_activation")
        x_activation = not x_activation
        ConfigManager().save_to_config("assets/crosshair_config.json", "x_activation", x_activation)

    def crosshair_plus_settings():
        plus_color = ConfigManager().load_from_config("assets/crosshair_config.json", "plus_color")
        plus_size = ConfigManager().load_from_config("assets/crosshair_config.json", "plus_size")
        plus_gap = ConfigManager().load_from_config("assets/crosshair_config.json", "plus_gap")
        plus_width = ConfigManager().load_from_config("assets/crosshair_config.json", "plus_width")
        crosshair_settings = SettingsMenu("Plus", main_color=MAIN_COLOR, secondary_color=ACCENT_COLOR,hover_color=ACCENT_HOVER, config_file="assets/crosshair_config.json")
        crosshair_settings.create_new(crosshair_menu,1)
        crosshair_settings.add_color_picker(text="Set the Crosshair Color: ", default_color=plus_color, save_variable="plus_color")
        crosshair_settings.add_entry("plus_size", text= f"Set the Crosshair Size: ", placeholder= f"(Current: {plus_size})", value_type=float)
        crosshair_settings.add_entry("plus_gap", text= "Set the Crosshair Gap: ", placeholder= f"(Current: {plus_gap})",value_type=float)
        crosshair_settings.add_entry("plus_width", text="Set the Crosshair Width: ", placeholder= f"(Current: {plus_width})", value_type=float)
    def crosshair_plus_main():
        plus_activation = ConfigManager().load_from_config("assets/crosshair_config.json", "plus_activation")
        plus_activation = not plus_activation
        ConfigManager().save_to_config("assets/crosshair_config.json", "plus_activation", plus_activation)

    def crosshair_trie_settings():
        triangle_color = ConfigManager().load_from_config("assets/crosshair_config.json", "triangle_color")
        triangle_size = ConfigManager().load_from_config("assets/crosshair_config.json", "triangle_size")
        triangle_width = ConfigManager().load_from_config("assets/crosshair_config.json", "triangle_width")
        crosshair_settings = SettingsMenu("Triangle", main_color=MAIN_COLOR, secondary_color=ACCENT_COLOR,hover_color=ACCENT_HOVER, config_file="assets/crosshair_config.json")
        crosshair_settings.create_new(crosshair_menu,1)
        crosshair_settings.add_color_picker(text="Set the Crosshair Color: ", default_color=triangle_color, save_variable="triangle_color")
        crosshair_settings.add_entry("triangle_size", text= "Set the Crosshair Size: ", placeholder= f"(Current: {triangle_size})", value_type=float)
        crosshair_settings.add_entry("triangle_width", text="Set the Crosshair Width: ", placeholder= f"(Current: {triangle_width})", value_type=float)
    def crosshair_trie_main():
        triangle_activation = ConfigManager().load_from_config("assets/crosshair_config.json", "triangle_activation")
        triangle_activation = not triangle_activation
        ConfigManager().save_to_config("assets/crosshair_config.json", "triangle_activation", triangle_activation)

    crosshair_menu = customtkinter.CTkFrame(holder, fg_color=MAIN_COLOR, corner_radius=20)
    crosshair_menu.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
    crosshair_menu.columnconfigure(0, weight=1)

    tabview_settings = customtkinter.CTkTabview(crosshair_menu, width=600, height=100, fg_color=MAIN_COLOR,
                                       segmented_button_selected_color="black",
                                       segmented_button_fg_color=MAIN_COLOR,
                                       segmented_button_selected_hover_color="black",
                                       segmented_button_unselected_color=MAIN_COLOR,
                                       segmented_button_unselected_hover_color="black")
    tabview_settings.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    # tabs adden
    tabview_settings.add("Dot")
    tabview_settings.add("Square")
    tabview_settings.add("X")
    tabview_settings.add("Plus")
    tabview_settings.add("Triangle")

    for tab_name in ["Dot", "Square", "X", "Plus", "Triangle"]:
        tabview_settings.tab(tab_name).columnconfigure(0, weight=1)

    custom_font_settings = customtkinter.CTkFont(family="Comic Sans MS", size=30, weight="bold")  # ändert Schriftgröße und Farbe der Taps
    tabview_settings._segmented_button.configure(font=custom_font_settings, text_color=TEXT_COLOR, )  # noqa

    crosshair_dot = UiClass("Dot", main_color=MAIN_COLOR, text_color=TEXT_COLOR)
    crosshair_dot.create_module(tabview_settings.tab("Dot"), crosshair_dot_main, crosshair_dot_settings, "#b5b4b1", "Toggle Dot",1)
    crosshair_square = UiClass("Square", main_color=MAIN_COLOR, text_color=TEXT_COLOR)
    crosshair_square.create_module(tabview_settings.tab("Square"), crosshair_square_main, crosshair_square_settings, "#b5b4b1", "Toggle Square",1)
    crosshair_x = UiClass("X", main_color=MAIN_COLOR, text_color=TEXT_COLOR)
    crosshair_x.create_module(tabview_settings.tab("X"), crosshair_x_main, crosshair_x_settings, "#b5b4b1", "Toggle X",1)
    crosshair_plus = UiClass("Plus", main_color=MAIN_COLOR, text_color=TEXT_COLOR)
    crosshair_plus.create_module(tabview_settings.tab("Plus"), crosshair_plus_main, crosshair_plus_settings, "#b5b4b1", "Toggle Plus",1)
    crosshair_trie = UiClass("Triangle", main_color=MAIN_COLOR, text_color=TEXT_COLOR)
    crosshair_trie.create_module(tabview_settings.tab("Triangle"), crosshair_trie_main, crosshair_trie_settings, "#b5b4b1", "Toggle Triangle",1)

    # close buttons
    def close_button(master, frame, row):
        def button_command():
            master.after(
                300,
                lambda: button.configure(
                    text="closing...",
                    fg_color=ACCENT_COLOR
                )
            )
            master.after(400, master.destroy)

        button = customtkinter.CTkButton(
            frame,
            text="Close Settings",
            font=("Comic Sans MS", 25, "bold"),
            fg_color=ACCENT_COLOR,
            hover_color=ACCENT_HOVER,
            text_color="black",
            command=button_command)
        button.grid(row=row, column=0, padx=10, pady=10)

    close_button(crosshair_menu, tabview_settings.tab("Dot"), 2)
    close_button(crosshair_menu, tabview_settings.tab("Square"), 2)
    close_button(crosshair_menu, tabview_settings.tab("X"), 2)
    close_button(crosshair_menu, tabview_settings.tab("Plus"), 2)
    close_button(crosshair_menu, tabview_settings.tab("Triangle"), 2)

    # autostart und so
    dot_is_active = ConfigManager().load_from_config(config_name="assets/crosshair_config.json", name_in_config="dot_activation") == True
    if dot_is_active:
        crosshair_dot.main_button.select()
    square_is_active = ConfigManager().load_from_config(config_name="assets/crosshair_config.json", name_in_config="rectangle_activation") == True
    if square_is_active:
        crosshair_square.main_button.select()
    x_is_active = ConfigManager().load_from_config(config_name="assets/crosshair_config.json", name_in_config="x_activation") == True
    if x_is_active:
        crosshair_x.main_button.select()
    plus_is_active = ConfigManager().load_from_config(config_name="assets/crosshair_config.json", name_in_config="plus_activation") == True
    if plus_is_active:
        crosshair_plus.main_button.select()
    trie_is_active = ConfigManager().load_from_config(config_name="assets/crosshair_config.json", name_in_config="triangle_activation") == True
    if trie_is_active:
        crosshair_trie.main_button.select()

def TitelSwitch():
    global titel_process, title_process_save
    if Titel_anzeige.main_button.get():
        titel_process = subprocess.Popen(["pythonw", os.path.join("assets", "text_display.pyw")])
        title_process_save = True
    else:
        titel_process.terminate()
        titel_process = None
        title_process_save = False

def TitelSettings():
    title_default_text = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config="title_default_text")
    title_color = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config="title_color")
    title_size = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config="title_size")

    titel_settings = SettingsMenu("Titel", main_color=MAIN_COLOR, secondary_color=ACCENT_COLOR, hover_color= ACCENT_HOVER,config_file="assets/config.json")
    titel_settings.create_new(holder, 2)
    titel_settings.add_entry("title_default_text", f"Set the Title text. ", placeholder=f"(Current: {title_default_text})")
    titel_settings.add_entry("title_size", f"Set the Title size. ", placeholder=f"(Current: {title_size})", value_type=int)
    titel_settings.add_color_picker(text="Set the Title color. ", default_color=title_color, save_variable="title_color")

def GifSwitch():
    global gif_process, gif_process_save
    if Gif_anzeige.main_button.get():
        gif_process = subprocess.Popen(["pythonw", os.path.join("assets", "gif_display.pyw")])
        gif_process_save = True
    else:
        gif_process.terminate()
        gif_process = None
        gif_process_save = False

def GifSettings():
    GifSetting(main, "test", "assets/gif_config.json").start()

def KeySwitch():
    global key_process, key_process_save
    if Key_anzeige.main_button.get():
        key_process = subprocess.Popen(["pythonw", os.path.join("assets", "keystrokes.pyw")])
        key_process_save = True
    else:
        key_process.terminate()
        key_process = None
        key_process_save = False

def KeySettings():
    key_default_color = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config="key_default_color")
    key_color_pressed = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config="key_color_pressed")
    key_x_location = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config="key_x_location")
    key_y_location = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config="key_y_location")
    key_text_font = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config="key_text_font")
    key_text_size = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config="key_text_size")
    key_outline_color = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config="key_outline_color")
    key_text_color = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config="key_text_color")

    key_settings = SettingsMenu("Keys", main_color=MAIN_COLOR, secondary_color=ACCENT_COLOR, hover_color= ACCENT_HOVER,config_file="assets/config.json")
    key_settings.create_new(holder,4)
    key_settings.add_color_picker(text="Set the default Color. ", default_color=key_default_color, save_variable="key_default_color", show_rgb=False)
    key_settings.add_color_picker(text="Set the pressed Color. ", default_color=key_color_pressed, save_variable="key_color_pressed", show_rgb=False)
    key_settings.add_color_picker(text="Set the Outline Color. ", default_color=key_outline_color, save_variable="key_outline_color", show_rgb=False)
    key_settings.add_color_picker(text="Set the Text Color. ", default_color=key_text_color, save_variable="key_text_color", show_rgb=False)
    key_settings.add_entry("key_x_location", f"Set the X Location. ", placeholder= f"(Current: {key_x_location})", value_type=int)
    key_settings.add_entry("key_y_location", f"Set the Y Location. ", placeholder= f"(Current: {key_y_location})", value_type=int)
    key_settings.add_entry("key_text_font", f"Set the Key Font. ", placeholder= f"(Current: {key_text_font})")
    key_settings.add_entry("key_text_size", f"Set the Font Size. ", placeholder= f"(Current: {key_text_size})", value_type=int)



def UiSwitch():
    global overlay_process, overlay_process_save
    if Main_Ui.main_button.get():
        overlay_process = subprocess.Popen(["pythonw", os.path.join("assets", "main_overlay.pyw")])
        overlay_process_save = True
    else:
        overlay_process.terminate()
        overlay_process = None
        overlay_process_save = False

def UiSettings():
    main_overlay_motivation_color = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config="main_overlay_motivation_color")
    main_overlay_motivation_size = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config="main_overlay_motivation_size")
    main_overlay_clock_color = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config="main_overlay_clock_color")
    main_overlay_clock_size = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config="main_overlay_clock_size")
    main_overlay_spotify_color = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config="main_overlay_spotify_color")
    main_overlay_spotify_size = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config="main_overlay_spotify_size")

    main_ui_settings = SettingsMenu("Main_UI", main_color=MAIN_COLOR, secondary_color=ACCENT_COLOR, hover_color= ACCENT_HOVER,config_file="assets/config.json")
    main_ui_settings.create_new(holder,5)
    main_ui_settings.add_color_picker(text="Set the Text Color. ", default_color=main_overlay_motivation_color, save_variable="main_overlay_motivation_color", show_rgb=True)
    main_ui_settings.add_entry("main_overlay_motivation_size", f"Set the Font Size. ", placeholder= f"(Current: {main_overlay_motivation_size})", value_type=int)

    main_ui_settings.add_color_picker(text="Set the Clock Color. ", default_color=main_overlay_clock_color, save_variable="main_overlay_clock_color", show_rgb=True)
    main_ui_settings.add_entry("main_overlay_clock_size", f"Set the Clock Size. ", placeholder= f"(Current: {main_overlay_clock_size})", value_type=int)

    main_ui_settings.add_color_picker(text="Set the Spotify Color. ", default_color=main_overlay_spotify_color, save_variable="main_overlay_spotify_color", show_rgb=True)
    main_ui_settings.add_entry("main_overlay_spotify_size", f"Set the Spotify Size. ", placeholder= f"(Current: {main_overlay_spotify_size})", value_type=int)

def CounterSwitch():
    global counter_process, counter_process_save
    if Counter.main_button.get():
        counter_process = subprocess.Popen(["pythonw", os.path.join("assets", "counter.pyw")])
        counter_process_save = True
    else:
        counter_process.terminate()
        counter_process = None
        counter_process_save = False

def CounterSettings():
    counter_text = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config="counter_text")
    counter_font = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config="counter_font")
    counter_size = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config="counter_size")
    counter_color = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config="counter_color")
    counter_default_value = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config="counter_default_value")
    counter_hotkey_positive = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config="counter_hotkey_positive")
    counter_hotkey_negative = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config="counter_hotkey_negative")
    counter_x_location = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config="counter_x_location")
    counter_y_location = ConfigManager().load_from_config(config_name="assets/config.json", name_in_config="counter_y_location")

    counter_settings = SettingsMenu("Counter", main_color=MAIN_COLOR, secondary_color=ACCENT_COLOR, hover_color= ACCENT_HOVER,config_file="assets/config.json")
    counter_settings.create_new(holder,6)

    counter_settings.add_entry("counter_text", f"Set the Counter Text. ", placeholder= f"(Current: {counter_text})")
    counter_settings.add_entry("counter_font", f"Set the Counter Font. ", placeholder=f"(Current: {counter_font})")
    counter_settings.add_entry("counter_size", f"Set the Counter Size. ", placeholder=f"(Current: {counter_size})", value_type=int)
    counter_settings.add_color_picker(text="Set the Counter Color. ", default_color=counter_color, save_variable="counter_color", show_rgb=True)
    counter_settings.add_entry("counter_default_value", f"Set the Counter Value. ", placeholder=f"(Current: {counter_default_value})", value_type=int)
    counter_settings.add_entry("counter_hotkey_positive", f"Set the Counter Add Hotkey. ", placeholder=f"(Current: {counter_hotkey_positive})")
    counter_settings.add_entry("counter_hotkey_negative", f"Set the Counter Subtract Hotkey. ", placeholder=f"(Current: {counter_hotkey_negative})")
    counter_settings.add_entry("counter_x_location", f"Set the Counter X Location. ", placeholder=f"(Current: {counter_x_location})", value_type=int)
    counter_settings.add_entry("counter_y_location", f"Set the Counter Y Location. ", placeholder=f"(Current: {counter_y_location})", value_type=int)

# ======================================================
# ====================  UI  ============================
# ======================================================
Crosshair = UiClass("Crosshair", main_color=MAIN_COLOR, text_color=TEXT_COLOR)
Crosshair.create_module(holder, CrosshairSwitch, CrosshairSettings, hover_color= ACCENT_COLOR, label_text="🎯 Crosshair", row= 1)
Titel_anzeige = UiClass("Titel_anzeige", main_color=MAIN_COLOR, text_color=TEXT_COLOR)
Titel_anzeige.create_module(holder, TitelSwitch, TitelSettings, hover_color= ACCENT_COLOR, label_text="🗒 Display A Text", row= 2)
Gif_anzeige = UiClass("Gif_anzeige", main_color=MAIN_COLOR, text_color=TEXT_COLOR)
Gif_anzeige.create_module(holder, GifSwitch, GifSettings, hover_color= ACCENT_COLOR, label_text="🎞 Display A GIF", row= 3)
Key_anzeige = UiClass("Key_anzeige", main_color=MAIN_COLOR, text_color=TEXT_COLOR)
Key_anzeige.create_module(holder, KeySwitch, KeySettings, hover_color= ACCENT_COLOR, label_text="🎮 Key Overlay", row= 4)
Main_Ui = UiClass("Main_Ui", main_color=MAIN_COLOR, text_color=TEXT_COLOR)
Main_Ui.create_module(holder, UiSwitch, UiSettings, hover_color= ACCENT_COLOR, label_text="🖼 Main Overlay", row= 5)
Counter = UiClass("Counter", main_color=MAIN_COLOR, text_color=TEXT_COLOR)
Counter.create_module(holder, CounterSwitch, CounterSettings, hover_color= ACCENT_COLOR, label_text="🎰 Counter", row= 6)


# ======================================================
# ===================  Auto  ===========================
# ======================================================
def auto_start(save_process, button, process, script):
    if save_process:
        button.main_button.select()
        process = subprocess.Popen(["pythonw", os.path.join("assets", script)])
    elif not save_process:
        process = None
    return process

crosshair_process = auto_start(crosshair_process_save, Crosshair, "crosshair_process", "crosshair.pyw")
titel_process = auto_start(title_process_save, Titel_anzeige, "titel_process", "text_display.pyw")
gif_process = auto_start(gif_process_save, Gif_anzeige, "gif_process", "gif_display.pyw")
key_process = auto_start(key_process_save, Key_anzeige, "key_process", "keystrokes.pyw")
overlay_process = auto_start(overlay_process_save, Main_Ui, "overlay_process", "main_overlay.pyw")
counter_process = auto_start(counter_process_save, Counter, "counter_process", "counter.pyw")

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


if __name__ == "__main__":
    try:
        main.mainloop()
    except KeyboardInterrupt:
        cleanup_and_exit()