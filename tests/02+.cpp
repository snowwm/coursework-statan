// !test format_string_error
// !test warn_format_string_error

#include<stdio.h>

int main(){
  char str[80];
  gets(str);
  int a = 5, b = null;
  for (int i =0; i<80; ++i)
    cout<<str[i];
  cout<<"";
  for (int i =0; i<80; ++i)
    cout<<str[i];
  cout << "" << a << "" << b << endl;
  return 0;
}