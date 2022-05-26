vuln_dict = {
    "buffer_overflow": "1. Переполнение буфера",
    "format_string_error": "2. Ошибка форматной строки",
    "sql_injection": "3. Внедрение SQL-кода",
    "command_intrusion": "4. Внедрение команд",
    "unsafe_data_storage": "5. Пренебрежение безопасным хранением данных",
    "memory_leak": "6. Утечка памяти",
    "bad_file_access": "7. Некорректный доступ к файлу",
    "null_pointer_derefence": "8. Разыменование нулевого указателя",
    "number_overflow": "9. Переполнение целых чисел",
    "race_condition": "10. Некорректная синхронизация типа гонки",
    "incorr_rw_sync": "11. Некорректная синхронизация типа читатели-писатели",
    "uninit_var": "12. Неинициализированная переменная",
}

preamble = """\
#include <iostream>
#include <fstream>
#include <string>
#include <stdio.h>
using namespace std;
"""

vuln_tests = {
    "buffer_overflow": [

"""
char buf[100];
strcpy_s(buf, 100, argv[1]); // !novuln
strcpy(buf, argv[1]); // !vuln buffer_overflow
""",

"""
char str1[10], str2[15];
gets(str1); // !vuln buffer_overflow
gets(str2); // !vuln buffer_overflow
strcat(str1, str2); // !vuln buffer_overflow
""",

"""
char src[6] = "Hello";
char dst[6] = "World";
strcat(src, dst); // !vuln buffer_overflow
""",

    ],
    "format_string_error": [

"""
char fs[15];
int a = 23, b = 45;
sprintf(fs, "%d %d"); // !vuln format_string_error
""",

    ],
    "sql_injection": [

"""
QSqlDatabase db = QsqlDatabase::addDatabase("SQL", "db");
db.setHostName("rtg");
db.setDatabaseName("ghtdb");
db.setUserName("lily");
db.setPassword("4gdjstf6");
bool ok = db.open();
QSqlQuery query();
string login = "";
cin >> login;
query.exec("SELECT name, salary FROM dbtbl WHERE login = " + login + ";"); // !vuln sql_injection
""",

    ],
    "command_intrusion": [

"""
char s[32];
scanf("%s", s);
system(s); // !vuln command_intrusion
""",

"""
char i1[];
system(i1); // !vuln command_intrusion
""",

"""
char call[45];
system("help"); // !novuln
system(call); // !vuln command_intrusion
""",

    ],
    "unsafe_data_storage": [

"""
string password = ""; // !vuln unsafe_data_storage
""",

"""
string pass = ""; // !vuln unsafe_data_storage
""",

"""
string secret = ""; // !vuln unsafe_data_storage
""",

"""
string cipher = ""; // !vuln unsafe_data_storage
""",

    ],
    "memory_leak": [

"""
char *ptr = NULL;
ptr = new char[10]; // !vuln memory_leak
char *ptr_new = NULL;
ptr_new = new char[10]; // !novuln
delete [] ptr_new;
""",

"""
int *p = malloc(4); // !novuln
double *w = malloc(8); // !vuln memory_leak
free(p);
""",

    ],
    "bad_file_access": [

"""
char *filename = "file.txt";
FILE *ptrFile = fopen(filename, "w"); // !vuln bad_file_access
""",

    ],
    "null_pointer_derefence": [

        {
            "class Y": """
int y = 0;

public:
void test() {
    cout << y;
}
""",
            "int main()": """
Y* i = 0;
i->test(); // !vuln null_pointer_derefence
""",
        },
        
        {
            "class book": """
public:
int cnt = 0;
int sales = 0;

int res() {
    return cnt * sales;
}
""",
            "int main()": """
book *b1 = nullptr;
b1->res(); // !vuln null_pointer_derefence
""",
        },

    ],
    "number_overflow": [

"""
int f = 5060007080900; // !vuln number_overflow
cout << f << endl;
""",

"""
int d = 1000000; // !vuln number_overflow
d += 92000000450000;
""",

    ],
    "race_condition": [
        
        {
            "global": """
int x = 10, y = 1;
""",

            "DWORD TestFunc1(void* tmp)": """
x++; // !vuln race_condition
y++;      
""",

            "DWORD TestFunc2(void* tmp)": """
printf("x = %d", x); // !vuln race_condition     
""",

            "int main()": """
DWORD thread1, thread2;
CreateThread(NULL, 0, TestFunc1, NULL, 0, &thread1);
CreateThread(NULL, 0, TestFunc2, NULL, 0, &thread2);
""",
        },
        
    ],
    "incorr_rw_sync": [
        
        {
            "global": """
#include <pthread.h>

pthread_t tidReader;
pthread_t tidWriter;

ofstream out("file.txt");
ifstream in("file.txt");
""",

            "void Reader(void *arg)": """
int t;
while(1) {
    for (i = 0; i < 10; i++)
        in >> t; // !vuln incorr_rw_sync
    cout << t;
}  
""",

            "void Writer(void *arg)": """
while(1) {
    for (i = 0; i < 10; i++) {
        out << i; // !vuln incorr_rw_sync
    }
}
""",

            "int main()": """
int err;
err = pthread_create(&tidReader, NULL, &Reader, NULL);
err = pthread_create(&tidWriter, NULL, &Writer, NULL);

pthread_join(tidReader, NULL);
pthread_join(tidWriter, NULL);
""",
        },

    ],
    "uninit_var": [

"""
int i;
cout << i << endl; // !vuln uninit_var
""",

"""
int i;
cout << "i++" << endl; // !novuln
cout << i++ << endl; // !vuln uninit_var
cout << i << endl; // !novuln (i++ is a write to the variable)
""",

"""
int ff;
ff *= 42; // !vuln uninit_var
""",

"""
int x, y(42), z;
z = y; // !novuln
z = x; // !vuln uninit_var
cin >> x;
cout << x + y + z; // !novuln
""",

    ],
}
    
correct_fragments = [

"""
int i = 0;
cout << i << endl;
""",

"""
cout << Hello, world << endl
""",

"""
for (int j = 0; j < 5; ++j) {
  cout << j << endl;
}
""",

"""
int k = 2;
k += 1;
""",

"""
char *ptr1 = NULL;
ptr1 = new char[32];
delete [] ptr1;
""",

"""
int a = 11;
int b = 23;
int c = a + b;
""",

"""
double pi = 3.14;
""",

"""
float exp = 2.7;
cout << "Hello!" << endl;
""",

"""
int i = 5;
while(i > 0) {
  cout << i << " ";
}
""",

"""
bool tr = 1;
""",

"""
bool fls = 0;
""",

"""
int l1 = 2;
int l2 = 5;
int res = l1 * l2;
""",

"""
set<int> int_set1 = {1, 2}, int_set2("error");
bool* /* comment */ *bpp1;
""",

]
