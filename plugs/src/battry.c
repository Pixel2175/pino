#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define BATTERY_PATH "/sys/class/power_supply/BAT1"
#define MAX_BUFFER 100

void pino(const char *title, const char *message) {
  char command[MAX_BUFFER * 2];
  snprintf(command, sizeof(command), "pino --title \"%s\" --massage \"%s\"",
           title, message);
  system(command);
}

int battery_capacity() {
  char path[MAX_BUFFER];
  snprintf(path, sizeof(path), "%s/capacity", BATTERY_PATH);

  FILE *file = fopen(path, "r");
  if (!file) {
    perror("Error opening capacity file");
    return -1;
  }

  int capacity;
  if (fscanf(file, "%d", &capacity) != 1) {
    perror("Error reading capacity");
    fclose(file);
    return -1;
  }

  fclose(file);
  return capacity;
}

char *battery_status() {
  char path[MAX_BUFFER];
  snprintf(path, sizeof(path), "%s/status", BATTERY_PATH);

  FILE *file = fopen(path, "r");
  if (!file) {
    perror("Error opening status file");
    return NULL;
  }

  static char status[MAX_BUFFER];
  if (fgets(status, sizeof(status), file) == NULL) {
    perror("Error reading status");
    fclose(file);
    return NULL;
  }

  status[strcspn(status, "\n")] = 0;

  fclose(file);
  return status;
}

int main() {
  int low_battery_warning = 0;
  int charging_warning = 0;
  int discharging_warning = 0;
  int full = 0;

  while (1) {
    int capacity = battery_capacity();
    char *status = battery_status();

    if (capacity <= 20 && strcmp(status, "Discharging") == 0 &&
        !low_battery_warning) {
      pino("Low Battery", "Plug Your Charger in");
      low_battery_warning = 1;
      charging_warning = 0;
    }

    if (strcmp(status, "Charging") == 0) {
      low_battery_warning = 0;
      discharging_warning = 0;
      full = 0;
      if (!charging_warning) {
        pino("Battery Charging", "The battery is charging now");
        charging_warning = 1;
      }
    }

    if (strcmp(status, "Discharging") == 0) {
      low_battery_warning = 0;
      charging_warning = 0;
      full = 0;
      if (!discharging_warning) {
        pino("Battery Discharging", "The battery is discharging now ");
        discharging_warning = 1;
      }
    }

    if (capacity == 100 && strcmp(status, "Not charging") == 0 && !full) {
      pino(" Battery Fully Charged", "You can unplug the charger now");
      full = 1;
    }

    usleep(50000);
  }

  return 0;
}
