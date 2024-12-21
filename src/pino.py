"""
PINO Tool:
  - Pino its a high customazabel app with low hardware usage and support pywal its a single file
  and its work in x11 and wayland normally without problems

  - to create a new notification u can use my Plugs or just create a scripts with any lang that u want
    that when your script run this app to show what u want thats all

REPORT:
  if u get some glitchs or something and u want to report it,
  just sent it to me in my DISCORD:pi66 and i will fix it

HOW TO USE IT:
  the app can handle 3 arguments:
    [1] --title   | will be set the string that u enter it to a title in the notification
    [2] --message | will be set the string that u enter it to a message in the notification
    [3] --config  | this is a optional its use if you want to set a special config file for the first run

  command:
    pino --title "enter you title" --message "enter your message" --config "enter a path for the config file that u want "



FUTURE:
- possiblity to add icon

"""

from customtkinter.windows.widgets import CTkFrame, CTkLabel
from customtkinter.windows.ctk_tk import CTk
from customtkinter.windows.ctk_input_dialog import CTkFont
from screeninfo.screeninfo import get_monitors
from json import load
from os.path import exists, expanduser
from os import getlogin, system
from argparse import ArgumentParser
# from threading import Thread
# from playsound import playsound


parsers = ArgumentParser(
    description="""This tool lets you display notification with  customizable options. 
you can also use a configuration file to set theme and everything easily (conf path = ~/.config/pino)"""
)

parsers.add_argument("--title", metavar="", help="set the notification title content")

parsers.add_argument(
    "--message", metavar="", help="set the notification message content"
)


parsers.add_argument(
    "--opacity",
    metavar="",
    help="set the opacity level for the window (range: 0 to 100)",
)

parsers.add_argument(
    "--delay", metavar="", help="set the delay before program closes with secends"
)
parsers.add_argument(
    "--sound",
    metavar="",
    help="set a custom sound file to play with notificaitons ( enable it in config file if its not )",
)
parsers.add_argument("--config", metavar="", help="set a custom configuration file ")


args = parsers.parse_args()
pywal_conf = None
conf = None
config_folder = f"/home/{getlogin()}/.config/pino/"

if not args.config:
    if exists(f"{config_folder}config.json"):
        with open(f"{config_folder}config.json", "r") as file:
            conf = load(file)
    else:
        system(f"mkdir {config_folder}  > /dev/null 2>&1")
        system(f"cp /etc/pino/config.json {config_folder} > /dev/null 2>&1")
        with open(f"{config_folder}config.json", "r") as file:
            conf = load(file)
else:
    with open(expanduser(args.config), "r") as file:
        conf = load(file)

if not exists(f"{config_folder}notification.mp3"):
    system(f"cp /etc/pino/notification.mp3 {config_folder} > /dev/null 2>&1")


sx = get_monitors()[conf["screen"]["monitor"]].x
sy = get_monitors()[conf["screen"]["monitor"]].y
sw = get_monitors()[conf["screen"]["monitor"]].width
sh = get_monitors()[conf["screen"]["monitor"]].height

ax = conf["screen"]["x"]
ay = conf["screen"]["y"]
aw = conf["screen"]["width"]
ah = conf["screen"]["height"]

V = conf["screen"]["vertical"]
H = conf["screen"]["horizontal"]

frame_fg = ""
border_color = ""
title_color = ""
message_color = ""


if conf["optional"]["pywal"]:
    with open(f"/home/{getlogin()}/.cache/wal/colors.json", "r") as file:
        pywal_conf = load(file)
    border_color = pywal_conf["colors"]["color1"]
    frame_fg = pywal_conf["colors"]["color0"]
    title_color = pywal_conf["special"]["cursor"]
    message_color = pywal_conf["colors"]["color8"]

else:
    border_color = conf["frame"]["border"]["color"]
    frame_fg = conf["frame"]["fg_color"]
    title_color = conf["title"]["color"]
    message_color = conf["message"]["color"]


def place():
    if V == "left".lower():
        if H == "top".lower():
            return f"{aw}x{ah}+{ax + sx}+{ay + sy}"
        elif H == "bottom".lower():
            return f"{aw}x{ah}+{sx + ax}+{sy + sh - ah - ay}"
    if V == "right".lower():
        if H == "top".lower():
            return f"{aw}x{ah}+{sx + sw - aw - ax }+{ay + sy}"
        elif H == "bottom".lower():
            return f"{aw}x{ah}+{sx + sw - aw - ax }+{sy + sh - ah - ay}"


class Main(CTk):
    def __init__(self):
        super().__init__()
        self.geometry(str(place()))
        self.resizable(False, False)
        self.overrideredirect(True)

        self.main = CTkFrame(
            width=aw,
            height=ah,
            master=self,
            border_width=conf["frame"]["border"]["width"],
            border_color=border_color,
            fg_color=frame_fg,
            corner_radius=conf["frame"]["border"]["border_radius"],
        )
        self.main.place(x=0, y=0)

        self.title = CTkLabel(
            self,
            text=f"{args.title} ",
            anchor="w",
            fg_color=frame_fg,
            text_color=title_color,
            width=aw
            - int(conf["frame"]["border"]["width"])
            - int(conf["title"]["x"] + 1),
            wraplength=(int(aw - conf["title"]["x"]) - 20)
            if (conf["title"]["wrap_length"] == "auto")
            else (int(conf["title"]["wrap_length"]) - 20),
            font=CTkFont(
                conf["frame"]["font_family"],
                conf["title"]["font_size"],
                conf["title"]["weigth"],
            ),
        )
        self.title.place(x=conf["title"]["x"], y=conf["title"]["y"])

        self.message = CTkLabel(
            self,
            text=f"{args.message} ",
            anchor="w",
            fg_color=frame_fg,
            text_color=message_color,
            width=aw
            - int(conf["frame"]["border"]["width"])
            - int(conf["message"]["x"] + 2),
            wraplength=(int(aw - conf["message"]["x"]) - 20)
            if (conf["message"]["wrap_length"] == "auto")
            else (int(conf["message"]["wrap_length"]) - 20),
            font=CTkFont(
                conf["frame"]["font_family"],
                conf["message"]["font_size"],
                conf["message"]["weigth"],
            ),
        )
        self.message.place(x=conf["message"]["x"], y=conf["message"]["y"])


if __name__ == "__main__":
    if args.message == None or args.title == None:
        parsers.print_help()
        exit()

    root = Main()
    root.after(
        30,
        lambda: root.attributes(
            "-alpha",
            int(args.opacity) / 100
            if args.opacity
            else conf["screen"]["opacity"] / 100,
        ),
    )
    root.after(
        int(args.delay) * 1000 if args.delay else conf["screen"]["show"] * 1000,
        root.quit,
    )

    if conf["optional"]["sound"]:
        from threading import Thread
        from playsound import playsound

        def start_sound(file):
            return Thread(target=lambda: playsound(file))

        thread = (
            start_sound(str(args.sound))
            if args.sound
            else start_sound(f"{config_folder}notification.mp3")
        )

        try:
            thread.start()
        except KeyboardInterrupt:
            exit()
    try:
        root.mainloop()
    except KeyboardInterrupt:
        exit()
