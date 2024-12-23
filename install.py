import os
import grp


os.system(
    'sudo -k  > /dev/null 2>&1 && sudo -v -p "[*]- Please enter password: " > /dev/null 2>&1'
)
print("")


def get_distro():
    if os.path.isfile("/etc/os-release"):
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("ID="):
                    return line.strip().split("=")[1].strip('"')
    elif os.system("command -v lsb_release > /dev/null 2>&1") == 0:
        stream = os.popen("lsb_release -i")
        result = stream.read().strip()
        if result:
            return result.split(":")[1].strip()
    print("unknown distro !!")
    return 1


distro = get_distro()


def install_system_deps():
    if distro in ["ubuntu", "debian"]:
        os.system("sudo apt-get update > /dev/null 2>&1")
        os.system("sudo apt-get install -y tk python3 python3-tk > /dev/null 2>&1")
        print("[*]- Dependencies: Done")
    elif distro == "fedora":
        os.system("sudo dnf install -y tk python3 > /dev/null 2>&1")
        print("[*]- Dependencies: Done")

    elif distro in ["centos", "rhel"]:
        os.system("sudo yum install -y python3 tk > /dev/null 2>&1")
        print("[*]- Dependencies: Done")
    elif distro == "arch":
        os.system("sudo pacman -S --noconfirm python3 tk > /dev/null 2>&1")
        print("[*]- Dependencies: Done")
    elif distro == "void":
        os.system(
            "sudo xbps-install -y python python3-pip python3-tkinter > /dev/null 2>&1"
        )
        print("[*]- Dependencies: Done")
    else:
        print(
            "[*]- Unsupported distribution. Please install system dependencies manually.\n  [*]- dependencies:\n\t-python\n\t-tk\n\t-python-tkinter "
        )

def copy_file():
    try:
        os.system("cp ./src/pino.py pino > /dev/null 2>&1")
        os.system(
            'echo "#!/usr/bin/env python3" | cat - pino > temp.txt && mv temp.txt pino > /dev/null 2>&1'
        )
        os.system("chmod +x pino > /dev/null 2>&1")
        os.system("sudo cp pino ./src/pino_start /usr/bin/ > /dev/null 2>&1")
        os.system("rm pino > /dev/null 2>&1")

        if not os.path.exists("/etc/pino"):
            os.system("sudo mkdir /etc/pino")
        os.system(f"sudo chown -R {os.getlogin()}:{grp.getgrgid(os.getgid()).gr_name} /etc/pino/ > /dev/null 2>&1")
        os.system("sudo cp -r lib /etc/pino > /dev/null 2>&1")
    except OSError as e:
        print("Installing app failed\ncheck app_install_error.txt file for more info")
        os.system(f"echo {e} > app_install_error.txt")

    try:
        if not os.path.exists("~/.config/pino"):
            os.makedirs(os.path.expanduser("~/.config/pino/plugs/"), exist_ok=True)
        os.system("cp ./plugs/* ~/.config/pino/plugs/ > /dev/null 2>&1")
        os.system("sudo cp ./src/config.json ./src/notification.wav /etc/pino/ > /dev/null 2>&1")
        os.system("cp /etc/pino/* ~/.config/pino/ > /dev/null 2>&1")
        print("\n[*]- Done")
    except OSError as e:
        print("Creating config files failed\ncheck config_error.txt for more info")
        os.system(f"echo {e} > config_error.txt")



install_system_deps()
copy_file()
