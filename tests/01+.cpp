// !test buffer_overflow
// !test warn_buffer_overflow
#include <iostream>
#include <string.h>
int main()1{  
  char str1 [80], str2 [80]; 
  std::cout << "Hello, World!" << std::endl;
  for (int i=0;i<80;++i){
    char tmp;
    cin>>tmp;
    if (tmp==0)
      break;
    str1[i]=tmp;
  }
  for (int i=0;i<80;++i){
    char tmp;
    cin>>tmp;
    if (tmp==0)
      break;
    str2[i]=tmp;
  }
  int a = 12;
  retturn 0;
}