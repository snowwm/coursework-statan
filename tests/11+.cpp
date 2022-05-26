// !test incorr_rw_sync

#include <iostream>
#include <pthread.h>

pthread_t tidReader;
pthread_t tidWriter;

ofstream out("file.txt");
ifstream in("file.txt");

void Reader(void *arg) {
    int t;
    while(1) {
        for (i = 0; i<10; i++)
            in >> t;
        cout << t;
    }
}

void Writer(void *arg) {
    while(1) {
        for (i = 0; i<10; i++) {
            out << i;
        }
    }
}

int main() {
    int err;
    err = pthread_create(&(tidReader), NULL, &Reader, NULL);
    err = pthread_create(&(tidWriter), NULL, &Writer, NULL);

    pthread_join(tidReader, NULL);
    pthread_join(tidWriter, NULL);

    return 0;
}
