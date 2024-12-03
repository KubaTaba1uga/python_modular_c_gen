#include <stdbool.h>
#include <string.h>
#include <time.h>

#include "std_lib_utils.h"

unsigned long get_current_time(void) {
  // Return number of seconds since Epoch.
  // On error returns 0.
  time_t now = time(NULL);
  if (now == (time_t)(-1))
    return 0;

  return (unsigned long)now;
}

bool are_strings_equal(char *str_a, char *str_b) {
  // Return True if A and B are equal, False otherwise.
  return strcmp(str_a, str_b) == 0;
}
