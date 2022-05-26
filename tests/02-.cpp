// !test format_string_error
// !test warn_format_string_error

#include<stdio.h>

int main(){
  char str[80];
  gets(str);
  int a = 5, b = null;
  sprintf(str,"%s %d %d", str, a, b);
  return 0;
}