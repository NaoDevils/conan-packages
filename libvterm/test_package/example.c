#include <vterm.h>
#include <string.h>

int main(void)
{
  VTerm* terminal = vterm_new(3, 10);
  if(!terminal)
    return 1;
  vterm_set_utf8(terminal, 1);
  VTermScreen* screen = vterm_obtain_screen(terminal);
  vterm_screen_reset(screen, 1);
  const char input[] = "Hi\x1b[31mR\r\n\xc3\xa4";
  vterm_input_write(terminal, input, strlen(input));
  vterm_screen_flush_damage(screen);
  VTermScreenCell cell;
  const VTermPos red = {0, 2};
  const VTermPos unicode = {1, 0};
  int passed = vterm_screen_get_cell(screen, red, &cell) && cell.chars[0] == 'R';
  passed = passed && vterm_screen_get_cell(screen, unicode, &cell) && cell.chars[0] == 0xe4;
  const char erase[] = "\x1b[2J";
  vterm_input_write(terminal, erase, strlen(erase));
  vterm_screen_flush_damage(screen);
  passed = passed && vterm_screen_get_cell(screen, red, &cell) && cell.chars[0] == 0;
  vterm_free(terminal);
  return passed ? 0 : 1;
}
