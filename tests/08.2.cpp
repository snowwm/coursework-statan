// !test null_pointer_derefence

#include <iostream>  // безуязвимости
    class Test{
    public:
        int a;
        int b;
        void printData(){
            cout << a << ", " << b << endl;
        }
        int setA(){
            return a;
        }
    };
    int main(){
        Test * tst = 0;
        cout << "Hello, world!" << endl;
        return 0;
    }