// !test memory_leak
#include <iostream>

using namespace std;

class TestClass{
public:
  iny x;
  int y;  
}
int main(){
  TestClass* ptr1 = new TestClass();
  TestClass* ptr2 = (TestClass*)malloc(sizeof(TestClass));
  free(ptr2);
  return 0;
}