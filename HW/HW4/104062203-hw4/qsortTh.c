#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

int *A; // array
pthread_mutex_t mutex1 = PTHREAD_MUTEX_INITIALIZER;
int maxthreads = 4;
int threadnum = 0;

int Partition(int p, int r) {
	// your code from Sec. 2.1 except array param is now global A
	int x = A[r];
	int i = p - 1;
	int j, temp;
	for(j = p; j < r; ++j){
		if(A[j] <= x){
			i += 1;
			temp = A[i];
			A[i] = A[j];
			A[j] = temp;
		}
	}
	temp = A[i+1];
	A[i+1] = A[r];
	A[r] = temp;
	return i + 1;
}
void* QuickSort(void *arg) {
	// your code
	int *a = (int*)arg;
	int p = a[0], r = a[1];
	if(p < r){
		int q = Partition(p, r);
		a[1] = q-1;
		if(threadnum <= maxthreads){
			pthread_t th;
			int ret = pthread_create(&th, NULL, QuickSort, a);
			threadnum++;
			if(ret != 0) {
                printf("Error: pthread_create() failed\n");
                exit(1);
        	}
        	pthread_join(th, NULL);
        	threadnum--;
		}
		else{
			QuickSort(a);
		}
		a[0] = q+1;
		a[1] = r;
		QuickSort(a);
	}
}
int main(int argc, char *argv[]) {
	// read randomInt.txt into array A
	// same as Sec 2.1.
	FILE* fh = fopen("randomInt.txt", "r");
	int len;
	fscanf(fh, "%d", &len);
	A = calloc(len, sizeof(int));
	for (int i = 0; i < len; i++) {
		fscanf(fh, "%d", A+i);
	}
	fclose(fh);
	int args[2] = { 0, len-1 };
	QuickSort(args);
	// check if they are sorted. This part is same as Sec 2.1
	for (int i = 0; i < len; i++) {
		if (A[i] != i) {
			fprintf(stderr, "error A[%d]=%d\n", i, A[i]);
		}
	}
}
