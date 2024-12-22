# Pino: Pixel Notification

Pino is a fully customizable notification tool that lets you display notifications with various options. It supports integration with Pywal to automatically match the notification theme to your wallpaper and includes customizable options for screen placement, fonts, and colors. You can also catch me in Discord: **@pi66** .

---

## Shortcuts
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Example: Low Battery Alert](#example-low-battery-alert)
- [System Startup](#system-startup)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Hardware Usage](#hardware-usage)

---

## Features
- **Customizable Notifications**: Set titles, messages, opacity, delay, sounds, and configuration files.
- **Dynamic Theming with Pywal**: Automatically matches the notification theme to your wallpaper.
- **Configurable Settings**: Adjust themes, screen placement, fonts, and more via JSON config files.
- **Script Integration**: Automate notifications using scripts in any language.
- **Pluggable Architecture**: Add custom scripts to the `~/.config/pino/plugs` directory.
- **System Start Scripts**: Use `pino_start` to initialize scripts at system startup.

---

## Installation

Run the `install.py` script to set up the application:

```bash
python install.py
```

---

## Dependencies

Pino requires the following dependencies:
- Python 3.6 or later
- Libraries listed in `requirements.txt` (installed via `pip install -r requirements.txt`)
- System tools: 
  - `python-tk` GUI Toolkit
- Optional: Pywal for dynamic theming

---

## Usage

Pino supports a variety of command-line options:

```bash
usage: pino [-h] [--title ] [--message ] [--opacity ] [--delay ] [--sound ] [--config ]

Options:
  -h, --help         Show this help message and exit
  --title            Set the notification title content
  --message          Set the notification message content
  --opacity          Set the opacity level for the window (range: 0 to 100)
  --delay            Set the delay before the program closes (in seconds)
  --sound            Set a custom sound file for notifications
  --config            Set a custom configuration file
```

### Example: Low Battery Alert
You can create a script to notify about [low battery status](https://github.com/Pixel2175/pino/blob/main/plugs/src/battery.c). Example in C:

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void pino(const char *title, const char *message) {
  char command[256];
  snprintf(command, sizeof(command), "pino --title \"%s\" --message \"%s\"", title, message);
  system(command);
}

int main() {
  pino("Low Battery", "Please plug your charger in!");
  return 0;
}
```

Compile and save the script to `~/.config/pino/plugs/`.

### System Startup
Add `pino_start` to your system startup to enable all scripts automatically.

---

## Configuration

The app uses a JSON configuration file located at `~/.config/pino/config.json`. Example:

```json
{
  "screen": {
    "monitor": 0,
    "vertical": "right",
    "horizontal": "top",
    "x": 20,
    "y": 20,
    "width": 300,
    "height": 100,
    "opacity": 100,
    "show": 3
  },
  "frame": {
    "fg_color": "#1a1e24",
    "font_family": "Fira Code",
    "border": {
      "width": 3,
      "color": "#566D8d",
      "border_radius": 10
    }
  },
  "title": {
    "color": "#c5c6c8",
    "font_size": 19,
    "x": 10,
    "y": 10,
    "weigth": "bold",
    "wrap_length": "auto"
  },
  "message": {
    "color": "#626977",
    "font_size": 15,
    "x": 15,
    "y": 45,
    "weigth": "normal",
    "wrap_length": "auto"
  },
  "optional": {
    "pywal": true,
    "sound": true
  }
}
```

---

## Hardware Usage

Pino is lightweight and efficient. The graphical notification window typically uses approximately **30MB of RAM** when active, ensuring minimal system resource consumption.

---
