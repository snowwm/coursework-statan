// !test not_safe_data_store
#include<iostream>
#include <fstream>
#include<string>

using namespace std;

int main(){
  string crypt = "";
  cout << "Введите crypt" << end;
  cin >> crypt;
  ofstream fout;
  fout.open("");
  fout << crypt;
  fout.close();
  return 0;
}