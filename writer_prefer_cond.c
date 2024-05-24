/*
 * alive 값이 true이면 각 스레드는 무한 루프를 돌며 반복해서 일을 하고,
 * alive 값이 false가 되면 무한 루프를 빠져나와 스레드를 자연스럽게 종료한다.
 */
bool alive = true;
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t w = PTHREAD_COND_INITIALIZER;
pthread_cond_t r = PTHREAD_COND_INITIALIZER;

int readers = 0; // 현재 활동중인 readers
int writers = 0; // 현재 활동중인 writers 
int waiting_writers = 0; // 현재 대기중인 writers 

void *reader(void *arg)
{
    int id, i;

    id = *(int *)arg;

    while (alive) {
        
    	pthread_mutex_lock(&mutex);
    	while (waiting_writers > 0 || writers > 0){ // 대기중인 writers 가 있거나, 활동중인 writers가 있다면, R이 기다린다. 
    		pthread_cond_wait(&r, &mutex);
    	}

    	readers++;

        while (readers == 1){ // reader가 1이라면, 임계구역에 진입하지 못하도록 W가 기다린다. 
    		pthread_cond_wait(&w, &mutex);
    	}
    	pthread_mutex_unlock(&mutex);
		// ���� �ִ��� ���� readers �� �� �� �ֵ��� mutex�� ����.  
        printf("<");
        for (i = 0; i < L0; ++i)
            printf("%c", 'A'+id);
        printf(">");
        
        
        pthread_mutex_lock(&mutex);
        readers--;
        
        if (readers == 0){ // 다 읽었으면은
        	pthread_cond_broadcast(&w); //W를 허용하기 위해서 W대기표를 모두 깨워서 뮤텍스락을 대기/얻을 수 있게 함.
        }
        pthread_mutex_unlock(&mutex);
        
        /* 
         * End Critical Section
         */
    }
    pthread_exit(NULL);
}

/*
 * Writer 스레드는 어떤 사람의 얼굴 이미지를 출력한다.
 * 이미지는 여러 종류가 있으며 인자를 통해 식별한다.
 * Writer가 critical section에 있으면 다른 writer는 물론이고 어떠한 reader도 들어올 수 없다.
 * 만일 이것을 어기고 다른 writer나 reader가 들어왔다면 얼굴 이미지가 깨져서 쉽게 감지된다.
 */
void *writer(void *arg)
{
    int id, i;
    struct timespec req;

    id = *(int *)arg;
    srand(time(NULL));

    while (alive) {
        
    	pthread_mutex_lock(&mutex);
    	waiting_writers++; 
		
  		while (waiting_writers > 0 || writers > 0){ // 첫 writer라면 임계구역에 진입하지못하도록 r을 대기시킨다. 
  			pthread_cond_wait(&r, &mutex);
  	 	}
  	 	
  	 	waiting_writers--; 
  	 	
  	   	while(writers == 1){ // �ȿ��� �������� writer�� �ִٸ� ��� ��� 
  	   		pthread_cond_wait(&w, &mutex);
		}
		writers++;
			 
        printf("\n");
        switch (id) {
            case 0:
                for (i = 0; i < L1; ++i)
                    printf("%s\n", img1[i]);
                break;
            case 1:
                for (i = 0; i < L2; ++i)
                    printf("%s\n", img2[i]);
                break;
            case 2:
                for (i = 0; i < L3; ++i)
                    printf("%s\n", img3[i]);
                break;
            case 3:
                for (i = 0; i < L4; ++i)
                    printf("%s\n", img4[i]);
                break;
            case 4:
                for (i = 0; i < L5; ++i)
                    printf("%s\n", img5[i]);
                break;
            default:
                ; 
        }

        writers--;
        
        if (waiting_writers > 0){ // 대기하고 있는 writer가 있다면 w를 깨우고. 
        	pthread_cond_signal(&w);
        }
        else{ // 대기하고 있는 writer가 없다면 r을 깨운다. 
        	pthread_cond_broadcast(&r);
        }

        pthread_mutex_unlock(&mutex);
        /* 
         * End Critical Section
         */
        /*
         * 이미지 출력 후 SLEEPTIME 나노초 안에서 랜덤하게 쉰다.
         */
        req.tv_sec = 0;
        req.tv_nsec = rand() % SLEEPTIME;
        nanosleep(&req, NULL);
    }
    pthread_exit(NULL);
}

/*
 * 메인 함수는 NREAD 개의 reader 스레드를 생성하고, NWRITE 개의 writer 스레드를 생성한다.
 * 생성된 스레드가 일을 할 동안 0.2초 동안 기다렸다가 alive의 값을 0으로 바꿔서 모든 스레드가
 * 무한 루프를 빠져나올 수 있게 만든 후, 스레드가 자연스럽게 종료할 때까지 기다리고 메인을 종료한다.
 */
int main(void)
{
    int i;
    int rarg[NREAD], warg[NWRITE];
    pthread_t rthid[NREAD];
    pthread_t wthid[NWRITE];
    struct timespec req;

    /*
     * Create NREAD reader threads
     */
    for (i = 0; i < NREAD; ++i) {
        rarg[i] = i;
        if (pthread_create(rthid+i, NULL, reader, rarg+i) != 0) {
            fprintf(stderr, "pthread_create error\n");
            return -1;
        }
    }
    /* 
     * Create NWRITE writer threads
     */
    for (i = 0; i < NWRITE; ++i) {
        warg[i] = i;
        if (pthread_create(wthid+i, NULL, writer, warg+i) != 0) {
            fprintf(stderr, "pthread_create error\n");
            return -1;
        }
    }
    /* 
     * Wait for RUNTIME nanoseconds while the threads are working
     */
    req.tv_sec = 0;
    req.tv_nsec = RUNTIME;
    nanosleep(&req, NULL);
    /*
     * Now terminate all threads and leave
     */
    pthread_mutex_lock(&mutex);
    alive = false;
    pthread_cond_broadcast(&r);
    pthread_cond_broadcast(&w);
    pthread_mutex_unlock(&mutex);
    
    for (i = 0; i < NREAD; ++i)
        pthread_join(rthid[i], NULL);
    for (i = 0; i < NWRITE; ++i)
        pthread_join(wthid[i], NULL);
        
    pthread_mutex_destroy(&mutex);
    pthread_cond_destroy(&r);
    pthread_cond_destroy(&w);
    
    
    return 0;
}
