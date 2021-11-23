#include <flite.h>
#include <stdio.h>

int main() {
  printf("  Carnegie Mellon University, Copyright (c) 1999-2016, all rights reserved\n");
  printf("  version: %s-%s-%s %s (http://cmuflite.org)\n", FLITE_PROJECT_PREFIX, FLITE_PROJECT_VERSION, FLITE_PROJECT_STATE, FLITE_PROJECT_DATE);

  int n;
  n = flite_init();
  printf("flite_init %i\n", n);
  n = flite_add_lang("eng", usenglish_init, cmulex_init);
  printf("flite_add_lang: %i\n", n);
  n = flite_add_lang("usenglish", usenglish_init, cmulex_init);
  printf("flite_add_lang: %i\n", n);
  
  return 0;
}
