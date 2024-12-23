import os

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


def install_pip():
    exit_code = os.system("pip3 --version > /dev/null 2>&1")
    if exit_code == 0:
        print("[*]- pip is installed !!")
    else:
        print("[*]- Pip not found. Installing pip...")
        print("[*]- wait...")
        if distro in ["ubuntu", "debian"]:
            os.system("sudo apt-get update")
            os.system("sudo apt-get install -y python3-pip > /dev/null 2>&1")
            print("[*]- pip installed Successfully !!")
        elif distro == "fedora":
            os.system("sudo dnf install -y python3-pip > /dev/null 2>&1")
            print("[*]- pip installed Successfully !!")
        elif distro in ["centos", "rhel"]:
            os.system("sudo yum install -y python3-pip > /dev/null 2>&1")
            print("[*]- pip installed Successfully !!")
        elif distro == "arch":
            os.system("sudo pacman -S --noconfirm python-pip > /dev/null 2>&1")
            print("[*]- pip installed Successfully !!")
        elif distro == "void":
            os.system("sudo xbps-install -y python3-pip > /dev/null 2>&1")
            print("[*]- pip installed Successfully !!")
        else:
            print("Unsupported distribution. Please install pip manually.")
            exit(1)


def install_system_deps():
    if distro in ["ubuntu", "debian"]:
        os.system("sudo apt-get update > /dev/null 2>&1")
        os.system("sudo apt-get install -y tk python python3-tk > /dev/null 2>&1")
        print("[*]- Dependencies: Done")
    elif distro == "fedora":
        os.system("sudo dnf install -y tk python > /dev/null 2>&1")
        print("[*]- Dependencies: Done")

    elif distro in ["centos", "rhel"]:
        os.system("sudo yum install -y python tk > /dev/null 2>&1")
        print("[*]- Dependencies: Done")
    elif distro == "arch":
        os.system("sudo pacman -S --noconfirm python tk > /dev/null 2>&1")
        print("[*]- Dependencies: Done")
    elif distro == "void":
        os.system(
            "sudo xbps-install -y tk python python-tkinter python3-tkinter > /dev/null 2>&1"
        )
        print("[*]- Dependencies: Done")
    else:
        print(
            "[*]- Unsupported distribution. Please install system dependencies manually.\n  [*]- dependencies:\n\t-python\n\t-tk\n\t-python-tkinter "
        )


def install_libs():
    try:
        os.system(
            "pip install --upgrade -y pip setuptools wheel --break-system-packages > /dev/null 2>&1"
        )
        print("[*]- Pip Upgraded Successfully !!")
    except OSError as e:
        print("[*]- Pip upgrade failed\ncheck pip_upgrade_error.txt for more info")
        os.system(f"echo {e} > pip_upgrade_error.txt")

    try:
        os.system(
            "pip install -r requirements.txt  --quiet --only-binary=:all: --break-system-packages"
        )
        print("[*]- Install libs successful !!")
    except OSError as e:
        print("[*]- Install libs failed !!\ncheck lib_install_error.txt for more info")
        os.system(f"echo {e} > lib_install_error.txt")


def copy_file():
    try:
        os.system("cp ./src/pino.py pino > /dev/null 2>&1")
        os.system(
            'echo "#!/usr/bin/env python3" | cat - pino > temp.txt && mv temp.txt pino > /dev/null 2>&1'
        )
        os.system("chmod +x pino > /dev/null 2>&1")
        os.system("sudo cp pino ./src/pino_start /usr/bin/ > /dev/null 2>&1")

        os.system("rm pino > /dev/null 2>&1")
    except OSError as e:
        print("Installing app failed\ncheck app_install_error.txt file for more info")
        os.system(f"echo {e} > app_install_error.txt")
    try:
        os.system("sudo mkdir /etc/pino/ > /dev/null 2>&1")
        os.system("mkdir -p ~/.config/pino/plugs/ > /dev/null 2>&1")
        os.system("cp ./plugs/* ~/.config/pino/plugs > /dev/null 2>&1")
        os.system(
            "sudo cp ./src/config.json ./src/notification.wav /etc/pino/ > /dev/null 2>&1"
        )
        os.system("cp /etc/pino/* ~/.config/pino/")
        print("\n[*]- Done")
    except OSError as e:
        print("Creating config files failed\ncheck config_error.txt for more info")
        os.system(f"echo {e} > config_error.txt")


install_pip()
install_libs()
install_system_deps()
copy_file()
