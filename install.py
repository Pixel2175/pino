import os

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
    return "unknown"


distro = get_distro()


def install_pip():
    exit_code = os.system("pip3 --version > /dev/null 2>&1")
    if exit_code == 0:
        print("Pip: Done")
    else:
        print("pip not found. Installing pip...")
        if distro in ["ubuntu", "debian"]:
            os.system("sudo apt-get update")
            os.system("sudo apt-get install -y python3-pip > /dev/null 2>&1")
            os.system("clear")
            print("Pip: Done")
        elif distro == "fedora":
            os.system("sudo dnf install -y python3-pip > /dev/null 2>&1")
            os.system("clear")
            print("Pip: Done")
        elif distro in ["centos", "rhel"]:
            os.system("sudo yum install -y python3-pip > /dev/null 2>&1")
            os.system("clear")
            print("Pip: Done")
        elif distro == "arch":
            os.system("sudo pacman -S --noconfirm python-pip > /dev/null 2>&1")
            os.system("clear")
            print("Pip: Done")
        elif distro == "void":
            os.system("sudo xbps-install -y python3-pip > /dev/null 2>&1")
            os.system("clear")
            print("Pip: Done")
        else:
            print("Unsupported distribution. Please install pip manually.")
            exit(1)


def install_system_deps():
    if distro in ["ubuntu", "debian"]:
        os.system("sudo apt-get update > /dev/null 2>&1")
        os.system("sudo apt-get install -y tk > /dev/null 2>&1")
        print("Dependencies: Done")
    elif distro == "fedora":
        os.system("sudo dnf install -y tk > /dev/null 2>&1")
        print("Dependencies: Done")

    elif distro in ["centos", "rhel"]:
        os.system("sudo yum install -y tk > /dev/null 2>&1")
        print("Dependencies: Done")
    elif distro == "arch":
        os.system("sudo pacman -S --noconfirm tk > /dev/null 2>&1")
        print("Dependencies: Done")
    elif distro == "void":
        os.system("sudo xbps-install -y tk > /dev/null 2>&1")
        print("Dependencies: Done")
    else:
        print("Unsupported distribution. Please install system dependencies manually.")


def install_libs():
    #
    os.system(
        "pip install --upgrade pip setuptools wheel --break-system-packages > /dev/null 2>&1"
    )
    os.system(
        "pip install customtkinter screeninfo playsound --only-binary=:all: --break-system-packages > /dev/null 2>&1 "
    )
    print("Libs: Done")


def copy_file():
    try:
        os.system("cp ./src/pino.py pino > /dev/null 2>&1")
        os.system(
            'echo "#!/usr/bin/env python3" | cat - pino > temp.txt && mv temp.txt pino > /dev/null 2>&1'
        )
        os.system("chmod +x pino > /dev/null 2>&1")
        os.system("sudo cp pino ./src/pino_start /usr/bin/ > /dev/null 2>&1")
        os.system("rm pino > /dev/null 2>&1")
        os.system("sudo mkdir /etc/pino/ > /dev/null 2>&1")
        os.system("mkdir ~/.config/pino/ ~/.config/pino/plugs/ > /dev/null 2>&1")
        os.system("cp ./plugs/* ~/.config/pino/plugs > /dev/null 2>&1")
        os.system(
            "sudo cp ./src/config.json ./src/notification.mp3 /etc/pino/ > /dev/null 2>&1"
        )
        print("\nAll Done")
    except:
        print("The file has not moved")


install_pip()
install_libs()
install_system_deps()
copy_file()
