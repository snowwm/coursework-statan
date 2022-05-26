// !test bad_file_access

#include<iostream> // суязвимостью

int main() {
string file_path = "";
char buf[50];
cin >> file_path;
FILE* file = fopen("file_path", "r"); 
while (!feof(file)) {
fgets(buf, 50, file);
cout << buf << endl;
}
getchar();
return 0;
}