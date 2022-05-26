// !test not_safe_data_store
#include<iostream>
#include <fstream>
#include<string>

using namespace std;

int main(){
  string absolute = "";
  cout << "Введите absolute" << end;
  cin >> absolute;
  ofstream fout;
  fout.open("");
  fout << absolute;
  fout.close();
  return 0;
}