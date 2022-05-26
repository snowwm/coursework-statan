// !test null_pointer_derefence

#include <iostream> // суязвимостью
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
        tst->printData();
        return 0;
    }