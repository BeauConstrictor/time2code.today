#include <sys/ioctl.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <unistd.h>
#include <signal.h>
#include <stdio.h>

#define MIN(a, b) ((a) < (b) ? (a) : (b))

// basically a histogram
void pprint(unsigned *nums, size_t count, unsigned max) {
    for (unsigned level = max; level > 0; level--) {
        for (size_t i = 0; i < count; i++) {
            if (nums[i] >= level)
                printf("| ");
            else
                printf("  ");
        }
        printf("\n");
    }

    for (size_t i = 0; i < count; i++)
        printf("--");
    printf("\n");
}

// fisher-yates
void shuffle(unsigned *nums, size_t count) {
    if (count < 2) return;
    for (size_t i = count - 1; i > 0; i--) {
        size_t j = rand() % (i + 1);

        unsigned tmp = nums[i];
        nums[i] = nums[j];
        nums[j] = tmp;
    }
}

bool is_sorted(unsigned *nums, size_t count) {
    for (size_t i = 1; i < count; i++) {
        if (nums[i - 1] > nums[i])
            return false;
    }

    return true;
}

// radix-sort
void sort(unsigned *nums, size_t count) {
  // these arrays actually only need to be count in length in total
  // between them, but we don't know where the split is. ones could
  // need count-1 items and zeroes could need just 1, so we go for
  // the longest they could possibly be.
  unsigned *ones   = malloc(sizeof(nums[0]) * count);
  unsigned *zeroes = malloc(sizeof(nums[0]) * count);

  for (int i = 0; i < sizeof(nums[0]) * CHAR_BIT; i++) {
    size_t one_count  = 0;
    size_t zero_count = 0;

    for (int n = 0; n < count; n++) {
      int  num = nums[n];
      bool bit = num & (1u << i);

      if (bit)
        ones[one_count++]    = num;
      else
        zeroes[zero_count++] = num;
    }

    // concatenate the two bit arrays, sorted
    size_t zeroes_size = zero_count * sizeof(zeroes[0]);
    size_t ones_size   = one_count  * sizeof(ones[0]);
    memcpy(nums, zeroes, zeroes_size);
    memcpy(nums+zero_count, ones, ones_size);

    printf("\033[2J\033[H");
    pprint(nums, count, count);
    usleep(400000);

    // we don't need this, it just stops the animation from staying
    // open for longer than needed.
    if (is_sorted(nums, count))
      break;
  }

  free(ones);
  free(zeroes);
}

void restore_terminal() {
  printf("\033[?1049l");
  exit(0);
}

int main(void) {
  struct winsize w;

  if (ioctl(STDOUT_FILENO, TIOCGWINSZ, &w) == -1) {
      perror("ioctl");
      return 1;
  }

  size_t n = MIN(w.ws_col/2, w.ws_row-2);
  unsigned nums[n];

  for (int i = 0; i < n; i++) {
    nums[i] = i;
  }

  printf("\033[?1049h");
  signal(SIGINT, restore_terminal);

  while (true) {
    shuffle(nums, n);

    sort(nums, n);
  }

  return 0;
}
