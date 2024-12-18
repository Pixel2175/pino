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
    [2] --massage | will be set the string that u enter it to a massage in the notification
    [3] --config  | this is a optional its use if you want to set a special config file for the first run

  command:
    pino --title "enter you title" --massage "enter your massage" --config "enter a path for the config file that u want "



FUTURE:
- possiblity to add icon

"""

from customtkinter import CTk, CTkFont, CTkFrame, CTkLabel
from screeninfo import get_monitors
from json import load
from os.path import exists, expanduser
from os import getlogin, system
from argparse import ArgumentParser
# from threading import Thread
# from playsound import playsound


parsers = ArgumentParser(description="Enter Title and Massage that you want to show")
parsers.add_argument("--title", metavar="", help="enter a string title")
parsers.add_argument("--massage", metavar="", help="enter a string massage")
parsers.add_argument(
    "--config", metavar="", help="to use a special config file 'optional'"
)
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
massage_color = ""


if conf["optional"]["pywal"]:
    with open(f"/home/{getlogin()}/.cache/wal/colors.json", "r") as file:
        pywal_conf = load(file)
    border_color = pywal_conf["colors"]["color1"]
    frame_fg = pywal_conf["colors"]["color0"]
    title_color = pywal_conf["special"]["cursor"]
    massage_color = pywal_conf["colors"]["color8"]

else:
    border_color = conf["frame"]["border"]["color"]
    frame_fg = conf["frame"]["fg_color"]
    title_color = conf["title"]["color"]
    massage_color = conf["massage"]["color"]


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

        self.massage = CTkLabel(
            self,
            text=f"{args.massage} ",
            anchor="w",
            fg_color=frame_fg,
            text_color=massage_color,
            width=aw
            - int(conf["frame"]["border"]["width"])
            - int(conf["massage"]["x"] + 2),
            wraplength=(int(aw - conf["massage"]["x"]) - 20)
            if (conf["massage"]["wrap_length"] == "auto")
            else (int(conf["massage"]["wrap_length"]) - 20),
            font=CTkFont(
                conf["frame"]["font_family"],
                conf["massage"]["font_size"],
                conf["massage"]["weigth"],
            ),
        )
        self.massage.place(x=conf["massage"]["x"], y=conf["massage"]["y"])


if __name__ == "__main__":
    if args.massage == None or args.title == None:
        parsers.print_help()
        exit()

    root = Main()
    root.after(30, lambda: root.attributes("-alpha", conf["screen"]["opacity"] / 100))
    root.after(conf["screen"]["show"] * 1000, root.quit)

    if conf["optional"]["sound"]:
        from threading import Thread
        from playsound import playsound

        thread = Thread(target=lambda: playsound(f"{config_folder}notification.mp3"))
        thread.start()

    root.mainloop()
