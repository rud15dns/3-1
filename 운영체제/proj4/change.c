bool alive = true;
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t read_phase = PTHREAD_COND_INITIALIZER;
pthread_cond_t write_phase = PTHREAD_COND_INITIALIZER;

int readers = 0;
int writers = 0;
int waiting_writers = 0;  // 대기 중인 writer 수

void *reader(void *arg)
{
    int id = *(int *)arg;

    while (alive) {
        pthread_mutex_lock(&mutex);
        
        while (waiting_writers > 0) {  // writer가 대기 중이면, reader는 대기
            pthread_cond_wait(&read_phase, &mutex);
        }
        
        readers++;
        if (readers == 1) {  // 첫 번째 reader가 들어왔을 때
            pthread_cond_wait(&write_phase, &mutex);  // writer 진입 차단
        }
        pthread_mutex_unlock(&mutex);

        // Critical section 시작
        printf("<");
        for (int i = 0; i < L0; ++i)
            printf("%c", 'A'+id);
        printf(">");

        pthread_mutex_lock(&mutex);
        readers--;
        if (readers == 0) {  // 마지막 reader가 나갔을 때
            pthread_cond_signal(&write_phase);  // writer 진입 허용
        }
        pthread_mutex_unlock(&mutex);
    }
    pthread_exit(NULL);
}

void *writer(void *arg)
{
    int id = *(int *)arg;

    while (alive) {
        pthread_mutex_lock(&mutex);
        
        waiting_writers++;
        if (writers == 0 && readers == 0) {  // 첫 번째 writer이고 reader가 없을 때
            pthread_cond_wait(&read_phase, &mutex);  // reader 진입 차단
        }
        writers++;
        pthread_mutex_unlock(&mutex);

        // Critical section 시작
        printf("\n");
        switch (id) {
            case 0:
                for (int i = 0; i < L1; ++i)
                    printf("%s\n", img1[i]);
                break;
            case 1:
                for (int i = 0; i < L2; ++i)
                    printf("%s\n", img2[i]);
                break;
            // 다른 케이스 생략
        }

        pthread_mutex_lock(&mutex);
        writers--;
        waiting_writers--;
        if (writers == 0 && waiting_writers == 0) {
            pthread_cond_broadcast(&read_phase);  // writer가 없으면 reader 진입 허용
        }
        pthread_mutex_unlock(&mutex);
    }
    pthread_exit(NULL);
}

// main 함수는 그대로 유지
