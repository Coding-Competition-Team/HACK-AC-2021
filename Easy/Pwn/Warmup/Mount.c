#include <stdio.h>
#include <signal.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

void timeout(int signum) {
    printf("Timeout!");
    exit(-1);
}

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    signal(SIGALRM, timeout);
    alarm(60);
}

void climb(){

	char altitude[64];
	int height = 0x73317331;

	printf("Where would you like to climb to?: ");

	fgets(altitude, 100, stdin);

	if(height != 0x73317331){
		system("cat flag.txt");
	}
	else{
		printf("Nowhere? sure");
	}
}

int main(int argc, char* argv[])
{
	setup();
	printf("Reach Mt. Stupid's summit and retrieve the flag!\n");
	climb();
	return 0;
}
