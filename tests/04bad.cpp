// !test command_intrusion
#include<iostream>
#include<string>
#include<unistd.h>
using namespace std;

int main(){
  char s[100];
  cout << "Введите строку: " << endl;
  cin >> s;
  system(s);
  retutn 0;
}