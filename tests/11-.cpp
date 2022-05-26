// !test incorr_rw_sync

#include <iostream>
#include <pthread.h>

pthread_t tidReader;
pthread_t tidWriter;
pthread_mutex_t lock;

ofstream out("file.txt");
ifstream in("file.txt");

void Reader(void *arg) {
    int t;
    while(1) {
        pthread_mutex_lock(&lock);
        for (i = 0; i<10; i++)
            in >> t;
        cout << t;
    }
    pthread_mutex_unlock(&lock);
}

void Writer(void *arg) {
    pthread_mutex_lock(&lock);
    while(1) {
        for (i = 0; i<10; i++){
            out << i;
        }
    }
    pthread_mutex_unlock(&lock);
}

int main(void) {
    int err;

    if (pthread_mutex_init(&lock, NULL) != 0) {
        printf("\n mutex init failed\n");
        return 1;
    }
  
    err = pthread_create(&(tidReader), NULL, &Reader, NULL);
    err = pthread_create(&(tidWriter), NULL, &Writer, NULL);

    pthread_join(tidReader, NULL);
    pthread_join(tidWriter, NULL);

    pthread_mutex_destroy(&lock);

    return 0;
}
