/*
 *
 * $Id: wrcmos.c,v 1.1 1998/09/24 21:08:20 hendriks Exp $
 */
#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <sys/io.h>

static inline
unsigned char readreg(int regno) {
  outb(regno, 0x70);
  return inb(0x71);
}

static inline
void writereg(int regno, unsigned char val) {
  outb(regno, 0x70);
  outb(val, 0x71);
}

unsigned char data[128];

int main(int argc, char *argv[]) {
  int i;
  if (ioperm(0x70, 2, 1) == -1) {
    perror("ioperm");
    exit(1);
  }
  
  read(STDIN_FILENO, data, sizeof(data));
  for (i=0; i < 128; i++) writereg(i, data[i]);

  exit(0);
}
