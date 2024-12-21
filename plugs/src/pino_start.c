#include <dirent.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

#define MAX_PATH_LENGTH 1024

int is_executable(const char *path) {
  struct stat st;

  // Check if file exists and is a regular file
  if (stat(path, &st) != 0) {
    return 0;
  }

  // Check if file is executable
  return (st.st_mode & S_IXUSR) || (st.st_mode & S_IXGRP) ||
         (st.st_mode & S_IXOTH);
}

int main() {
  const char *home_dir = getenv("HOME");
  if (home_dir == NULL) {
    fprintf(stderr, "Could not get HOME directory\n");
    return 1;
  }

  char plugs_dir[MAX_PATH_LENGTH];
  snprintf(plugs_dir, sizeof(plugs_dir), "%s/.config/pino/plugs/", home_dir);

  DIR *dir;
  struct dirent *entry;

  // Open directory
  dir = opendir(plugs_dir);
  if (dir == NULL) {
    fprintf(stderr, "Unable to open directory %s: %s\n", plugs_dir,
            strerror(errno));
    return 1;
  }

  // Read directory entries
  while ((entry = readdir(dir)) != NULL) {
    // Skip current and parent directory entries
    if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) {
      continue;
    }

    // Construct full path
    char full_path[MAX_PATH_LENGTH];
    snprintf(full_path, sizeof(full_path), "%s%s", plugs_dir, entry->d_name);

    // Check if file is executable
    if (is_executable(full_path)) {
      printf("Starting: %s\n", full_path);

      // Fork and execute
      pid_t pid = fork();

      if (pid == 0) {
        // Child process
        execl(full_path, full_path, NULL);

        // If execl fails
        fprintf(stderr, "Failed to execute %s\n", strerror(errno));
        exit(1);
      }
      // Parent process continues to next file
    }
  }

  // Close directory
  closedir(dir);

  printf("Finished.\n");

  return 0;
}
