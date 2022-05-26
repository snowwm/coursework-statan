// !test buffer_overflow
// !test warn_buffer_overflow
#include <iostream>
#include <string.h>

int main(){
  char str1 [80],str2[80];
  std::cout<<"Hello, World!"<<std::endl;
  gets(str1);
  gets(str2);
  int a=12;
  strcat(str2,str1);
  return 0;
}