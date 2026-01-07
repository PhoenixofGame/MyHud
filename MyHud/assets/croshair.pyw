import tkinter as tk
import json
import win32gui
import win32con
import colorsys
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

cross_config_path = os.path.join(BASE_DIR, "assets", "config.json")
activation_config_path = os.path.join(BASE_DIR, "assets", "config.json")

try:
    with open(cross_config_path, 'r') as f: # läd variablen
        daten = json.load(f)

    CrossDoTFarbe = daten["CrossDoTFarbe"] 
    CrossDoTOutline = daten["CrossDoTOutline"] 
    CrossDoTGrose = daten["CrossDoTGrose"] 
    CrossEckFarbe = daten["CrossEckFarbe"] 
    CrossEckOutline = daten["CrossEckOutline"] 
    CrossEckGrose = daten["CrossEckGrose"] 
    CrossXFarbe = daten["CrossXFarbe"] 
    CrossXGrose = daten["CrossXGrose"] 
    CrossXGap = daten["CrossXGap"] 
    CrossPFarbe = daten["CrossPFarbe"] 
    CrossPGrose = daten["CrossPGrose"] 
    CrossPGap = daten["CrossPGap"] 
    CrossDreiFarbe = daten["CrossDreiFarbe"] 
    CrossDreiGrose = daten["CrossDreiGrose"] 

except FileNotFoundError: # default Variablen falls config.json nicht exestiert
    CrossDoTFarbe = "white"
    CrossDoTOutline = "blue"
    CrossDoTGrose = 2.5
    CrossEckFarbe = "white"
    CrossEckOutline = "black"
    CrossEckGrose = 2.5
    CrossXFarbe = "blue"
    CrossXGrose = 2.5
    CrossXGap = 2.5
    CrossPFarbe = "white"
    CrossPGrose = 2.5
    CrossPGap = 2.5
    CrossDreiFarbe = "white"
    CrossDreiGrose = 2.5

try:
    with open(activation_config_path, 'r') as f: # läd variablen
        daten = json.load(f)
    DoTActivation = daten["DoTActivation"]     
    EckActivation = daten["EckActivation"] 
    PActivation = daten["PActivation"] 
    XActivation = daten["XActivation"] 
    DreiActivation = daten["DreiActivation"] 

except FileNotFoundError:
    DoTActivation = "Aus"
    EckActivation = "Aus"
    PActivation = "Aus"
    XActivation = "Aus"
    DreiActivation = "Aus"
    print ("Err")


toast = tk.Tk()
toast.title("CrosshairOverlay")
toast.attributes("-topmost", True)
toast.update()


toast.attributes("-transparentcolor", "#000001")  # Transparent background
toast.overrideredirect(True)  # Remove window border

# Make the window click-through
toast.update()
mainhwnd = win32gui.FindWindow(None, str(toast.title()))
exStyle = win32gui.GetWindowLong(mainhwnd, win32con.GWL_EXSTYLE)
exStyle |= win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
win32gui.SetWindowLong(mainhwnd, win32con.GWL_EXSTYLE, exStyle)

# fullscreen
screen_width = toast.winfo_screenwidth()
screen_height = toast.winfo_screenheight()
toast.geometry(f"{screen_width}x{screen_height}+0+0")


canvas = tk.Canvas(toast, width=screen_width, height=screen_height, bg="#000001", highlightthickness=0,)
canvas.pack()


if DoTActivation == "An":
    if CrossDoTFarbe != "rgb" and CrossDoTOutline != "rgb":
        # kreis crs
        canvas.create_oval(screen_width//2 - CrossDoTGrose,
                           screen_height//2 - CrossDoTGrose,
                           screen_width//2 + CrossDoTGrose,
                           screen_height//2 + CrossDoTGrose,
                           fill= CrossDoTFarbe, outline=CrossDoTOutline)

    elif CrossDoTFarbe == "rgb" and CrossDoTOutline == "rgb":
        txcolordot = []
        for i in range(360):
            h = i / 360.0
            r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
            txcolordot.append('#{0:02X}{1:02X}{2:02X}'.format(
                int(r * 255), int(g * 255), int(b * 255)
            ))
        index_dot = 0
        def update_color_dot():
            global index_dot
            TextColor = txcolordot[index_dot]
            canvas.itemconfig(mot_id_dot, fill=TextColor, outline=TextColor)
            index_dot = (index_dot + 1) % len(txcolordot)
            toast.after(16, update_color_dot)

        mot_id_dot = canvas.create_oval(screen_width//2 - CrossDoTGrose,
                                        screen_height//2 - CrossDoTGrose,
                                        screen_width//2 + CrossDoTGrose,
                                        screen_height//2 + CrossDoTGrose,
                                        fill= "white", outline="white")
        update_color_dot()

    elif CrossDoTFarbe == "rgb":
        txcolordot = []
        for i in range(360):
            h = i / 360.0
            r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
            txcolordot.append('#{0:02X}{1:02X}{2:02X}'.format(
                int(r * 255), int(g * 255), int(b * 255)
            ))
        index_dot = 0
        def update_color_dot():
            global index_dot
            TextColor = txcolordot[index_dot]
            canvas.itemconfig(mot_id_dot, fill=TextColor)
            index_dot = (index_dot + 1) % len(txcolordot)
            toast.after(16, update_color_dot)

        mot_id_dot = canvas.create_oval(screen_width//2 - CrossDoTGrose,
                                        screen_height//2 - CrossDoTGrose,
                                        screen_width//2 + CrossDoTGrose,
                                        screen_height//2 + CrossDoTGrose,
                                        fill= "white", outline=CrossDoTOutline)
        update_color_dot()

    elif CrossDoTOutline == "rgb":
        txcolordot = []
        for i in range(360):
            h = i / 360.0
            r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
            txcolordot.append('#{0:02X}{1:02X}{2:02X}'.format(
                int(r * 255), int(g * 255), int(b * 255)
            ))
        index_dot = 0
        def update_color_dot():
            global index_dot
            TextColor = txcolordot[index_dot]
            canvas.itemconfig(mot_id_dot, outline=TextColor)
            index_dot = (index_dot + 1) % len(txcolordot)
            toast.after(16, update_color_dot)

        mot_id_dot = canvas.create_oval(screen_width//2 - CrossDoTGrose,
                                        screen_height//2 - CrossDoTGrose,
                                        screen_width//2 + CrossDoTGrose,
                                        screen_height//2 + CrossDoTGrose,
                                        fill= CrossDoTFarbe, outline="white")
        update_color_dot()

else:
    pass

if EckActivation == "An":
    if CrossEckFarbe != "rgb" and CrossEckOutline != "rgb":
        # viereck crs
        canvas.create_rectangle(
            screen_width//2 - CrossEckGrose, screen_height//2 - CrossEckGrose,
            screen_width//2 + CrossEckGrose, screen_height//2 + CrossEckGrose,
            fill=CrossEckFarbe, outline=CrossEckOutline)

    elif CrossEckFarbe == "rgb" and CrossEckOutline == "rgb":
        txcoloreck = []
        for i in range(360):
            h = i / 360.0
            r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
            txcoloreck.append('#{0:02X}{1:02X}{2:02X}'.format(
                int(r * 255), int(g * 255), int(b * 255)
            ))
        index_eck = 0
        def update_color_eck():
            global index_eck
            TextColor = txcoloreck[index_eck]
            canvas.itemconfig(mot_id_eck, fill=TextColor, outline=TextColor)
            index_eck = (index_eck + 1) % len(txcoloreck)
            toast.after(16, update_color_eck)

        mot_id_eck = canvas.create_rectangle(screen_width//2 - CrossEckGrose, screen_height//2 - CrossEckGrose,
                                             screen_width//2 + CrossEckGrose, screen_height//2 + CrossEckGrose,
                                            fill="white", outline="white")
        update_color_eck()

    elif CrossEckFarbe == "rgb":
        txcoloreck = []
        for i in range(360):
            h = i / 360.0
            r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
            txcoloreck.append('#{0:02X}{1:02X}{2:02X}'.format(
                int(r * 255), int(g * 255), int(b * 255)
            ))
        index_eck = 0
        def update_color_eck():
            global index_eck
            TextColor = txcoloreck[index_eck]
            canvas.itemconfig(mot_id_eck, fill=TextColor)
            index_eck = (index_eck + 1) % len(txcoloreck)
            toast.after(16, update_color_eck)

        mot_id_eck = canvas.create_rectangle(screen_width//2 - CrossEckGrose, screen_height//2 - CrossEckGrose,
                                             screen_width//2 + CrossEckGrose, screen_height//2 + CrossEckGrose,
                                            fill="white", outline=CrossEckOutline)
        update_color_eck()

    elif CrossEckOutline == "rgb":
        txcoloreck = []
        for i in range(360):
            h = i / 360.0
            r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
            txcoloreck.append('#{0:02X}{1:02X}{2:02X}'.format(
                int(r * 255), int(g * 255), int(b * 255)
            ))
        index_eck = 0


        def update_color_eck():
            global index_eck
            TextColor = txcoloreck[index_eck]
            canvas.itemconfig(mot_id_eck, outline=TextColor)
            index_eck = (index_eck + 1) % len(txcoloreck)
            toast.after(16, update_color_eck)


        mot_id_eck = canvas.create_rectangle(screen_width // 2 - CrossEckGrose, screen_height // 2 - CrossEckGrose,
                                             screen_width // 2 + CrossEckGrose, screen_height // 2 + CrossEckGrose,
                                             fill=CrossEckFarbe, outline="white")
        update_color_eck()


else:
    pass

if XActivation == "An":
    if CrossXFarbe != "rgb":
        kombiniertX = CrossXGrose + CrossXGap
        # X crs
        canvas.create_line(screen_width//2 + CrossXGap, screen_height//2 + CrossXGap, screen_width//2 + kombiniertX, screen_height//2 + kombiniertX, fill=CrossXFarbe, width=2) # RECHTSHOCH
        canvas.create_line(screen_width//2 - CrossXGap, screen_height//2 + CrossXGap, screen_width//2 - kombiniertX, screen_height//2 + kombiniertX, fill=CrossXFarbe, width=2) # linkshoch
        canvas.create_line(screen_width//2 + CrossXGap, screen_height//2 - CrossXGap, screen_width//2 + kombiniertX, screen_height//2 - kombiniertX, fill=CrossXFarbe ,width=2) # rechtsrunter
        canvas.create_line(screen_width//2 - CrossXGap, screen_height//2 - CrossXGap, screen_width//2 - kombiniertX, screen_height//2 - kombiniertX, fill=CrossXFarbe ,width=2) # linksrunter

    elif CrossXFarbe == "rgb":
        kombiniertX = CrossXGrose + CrossXGap
        txcolorx = []
        for i in range(360):
            h = i / 360.0
            r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
            txcolorx.append('#{0:02X}{1:02X}{2:02X}'.format(
                int(r * 255), int(g * 255), int(b * 255)
            ))
        index_x = 0
        def update_color_x():
            global index_x
            TextColor = txcolorx[index_x]
            canvas.itemconfig(mot_id_x1, fill=TextColor)
            canvas.itemconfig(mot_id_x2, fill=TextColor)
            canvas.itemconfig(mot_id_x3, fill=TextColor)
            canvas.itemconfig(mot_id_x4, fill=TextColor)
            index_x = (index_x + 1) % len(txcolorx)
            toast.after(16, update_color_x)

        mot_id_x1 = canvas.create_line(screen_width//2 + CrossXGap, screen_height//2 + CrossXGap, screen_width//2 + kombiniertX, screen_height//2 + kombiniertX, fill="white", width=2) # RECHTSHOCH
        mot_id_x2 = canvas.create_line(screen_width//2 - CrossXGap, screen_height//2 + CrossXGap, screen_width//2 - kombiniertX, screen_height//2 + kombiniertX, fill="white", width=2) # linkshoch
        mot_id_x3 = canvas.create_line(screen_width//2 + CrossXGap, screen_height//2 - CrossXGap, screen_width//2 + kombiniertX, screen_height//2 - kombiniertX, fill="white", width=2) # rechtsrunter
        mot_id_x4 = canvas.create_line(screen_width//2 - CrossXGap, screen_height//2 - CrossXGap, screen_width//2 - kombiniertX, screen_height//2 - kombiniertX, fill="white", width=2) # linksrunter

        update_color_x()

else:
    pass

if PActivation == "An":
    if CrossPFarbe != "rgb":
        kombiniert = CrossPGrose + CrossPGap
        # + crs
        canvas.create_line(screen_width//2 - CrossPGap, screen_height//2, screen_width//2 - kombiniert, screen_height//2, fill=CrossPFarbe, width=2) # links
        canvas.create_line(screen_width//2, screen_height//2 - CrossPGap, screen_width//2, screen_height//2 - kombiniert, fill=CrossPFarbe, width=2) # runter
        canvas.create_line(screen_width//2 + CrossPGap, screen_height//2, screen_width//2 + kombiniert, screen_height//2, fill=CrossPFarbe, width=2) # rechts
        canvas.create_line(screen_width//2, screen_height//2 + CrossPGap, screen_width//2, screen_height//2 + kombiniert, fill=CrossPFarbe, width=2) # hoch


    elif CrossPFarbe == "rgb":
        kombiniert = CrossPGrose + CrossPGap
        txcolorplus = []
        for i in range(360):
            h = i / 360.0
            r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
            txcolorplus.append('#{0:02X}{1:02X}{2:02X}'.format(
                int(r * 255), int(g * 255), int(b * 255)
            ))
        index_plus = 0
        def update_color_plus():
            global index_plus
            TextColor = txcolorplus[index_plus]
            canvas.itemconfig(mot_id_p1, fill=TextColor)
            canvas.itemconfig(mot_id_p2, fill=TextColor)
            canvas.itemconfig(mot_id_p3, fill=TextColor)
            canvas.itemconfig(mot_id_p4, fill=TextColor)
            index_plus = (index_plus + 1) % len(txcolorplus)
            toast.after(16, update_color_plus)

        mot_id_p1 = canvas.create_line(screen_width//2 - CrossPGap, screen_height//2,   screen_width//2 - kombiniert, screen_height//2, fill="white", width=2) # links
        mot_id_p2 = canvas.create_line(screen_width // 2, screen_height // 2 - CrossPGap, screen_width // 2, screen_height // 2 - kombiniert, fill="white", width=2) # runter
        mot_id_p3 = canvas.create_line(screen_width // 2 + CrossPGap, screen_height // 2, screen_width // 2 + kombiniert, screen_height // 2, fill="white", width=2)  # rechts
        mot_id_p4 = canvas.create_line(screen_width // 2, screen_height // 2 + CrossPGap, screen_width // 2, screen_height // 2 + kombiniert, fill="white", width=2)  # hoch
        update_color_plus()

else:
    pass

if DreiActivation == "An":
    # dreieck
    if CrossDreiFarbe != "rgb":
        canvas.create_line(screen_width//2 + CrossDreiGrose, screen_height//2 + CrossDreiGrose, #linke ecke
                           screen_width//2 - CrossDreiGrose, screen_height//2 + CrossDreiGrose, # rechte ecke
                           screen_width//2, screen_height//2, #spitze
                           screen_width//2 + CrossDreiGrose, screen_height//2 + CrossDreiGrose, # linke ecke
                           width=5, fill=CrossDreiFarbe)

    elif CrossDreiFarbe == "rgb":
        txcolordrei = []
        for i in range(360):
            h = i / 360.0
            r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
            txcolordrei.append('#{0:02X}{1:02X}{2:02X}'.format(
                int(r * 255), int(g * 255), int(b * 255)
            ))
        index_drei = 0
        def update_color_drei():
            global index_drei
            TextColor = txcolordrei[index_drei]
            canvas.itemconfig(mot_id_drei, fill=TextColor)
            index_drei = (index_drei + 1) % len(txcolordrei)
            toast.after(16, update_color_drei)

        mot_id_drei =canvas.create_line(screen_width//2 + CrossDreiGrose, screen_height//2 + CrossDreiGrose, #linke ecke
                           screen_width//2 - CrossDreiGrose, screen_height//2 + CrossDreiGrose, # rechte ecke
                           screen_width//2, screen_height//2, #spitze
                           screen_width//2 + CrossDreiGrose, screen_height//2 + CrossDreiGrose, # linke ecke
                           width=5, fill="white")
        update_color_drei()

else:
    pass


def force_topmost():
    try:
        win32gui.SetWindowPos(
            mainhwnd,
            win32con.HWND_TOPMOST,
            0, 0, 0, 0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE
        )
        toast.after(500, force_topmost)
    except:
        pass

toast.after(100, force_topmost)
toast.mainloop()    