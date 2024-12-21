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


def remove_system_deps():
    if distro in ["ubuntu", "debian"]:
        os.system("sudo apt-get remove  -y tk > /dev/null 2>&1")
        print("Remove System Dep: Done")
    elif distro == "fedora":
        os.system("sudo dnf remove  -y tk > /dev/null 2>&1")
        print("Remove System Dep: Done")
    elif distro in ["centos", "rhel"]:
        os.system("sudo yum remove  -y tk > /dev/null 2>&1")
        print("Remove System Dep: Done")
    elif distro == "arch":
        os.system("sudo pacman -Rns --noconfirm tk > /dev/null 2>&1")
        print("Remove System Dep: Done")
    elif distro == "void":
        os.system("sudo xbps-remove -R -y tk > /dev/null 2>&1")
        print("Remove System Dep: Done")
    else:
        print("Unsupported distribution. Please install system dependencies manually.")


def uninstall_libs():
    os.system(
        "pip uninstall --yes customtkinter playsound screeninfo --break-system-packages > /dev/null 2>&1"
    )
    print("Remove Libs: Done")


def remove_files():
    try:
        os.system(
            "sudo rm -r /usr/bin/pino  /usr/bin/pino_start /etc/pino/ > /dev/null 2>&1"
        )
        os.system("rm -r ~/.config/pino/ ~/.config/pino/plugs/ > /dev/null 2>&1")
        print("Remove App: Done")
    except OSError:
        print("Faild remove")


remove_system_deps()
uninstall_libs()
remove_files()
