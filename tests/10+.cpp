// !test race_condition

int x = 10, y = 1;

DWORD WINAPI TestFunc1(void* tmp) {
    x++;
    y++;
}

DWORD WINAPI TestFunc2 (void* tmp) {
    if (x % 2 == 0) {
        x = x - 1;
        printf("x = %d\n", x);
    }
}

DWORD WINAPI TestFunc3 (void* tmp) {
    int a = 5;
    a += x + y;
    printf("a+x+y = %d\n", a);
}

int main() {
    DWORD thread1, thread2, thread3;
  
    CreateThread(NULL, 0, TestFunc1, NULL, 0, &thread1);
    CreateThread(NULL, 0, TestFunc2, NULL, 0, &thread2);
    CreateThread(NULL, 0, TestFunc3, NULL, 0, &thread3);
}
