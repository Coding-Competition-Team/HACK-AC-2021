#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <signal.h>

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

void die(){
	char buf[0x100];
	puts("Your Input: ");
	puts("Jokes on you, the buffer is size 0x100 but we're only reading 25 bytes HEHHEH");
	read(0,&buf,25);
	puts("Meh");
	printf(&buf);
	puts("Sure you can try to input again....");
	read(0,&buf,0x200);
	puts("Noted with Thanks");
	printf("Your Input: %s",&buf);
	return;
}

int main(){
	setup();
	puts("well we enabled every protection, PIE, ASLR, Canary, NX bit...");
	puts("What you gonna do now huh...");
	puts("Well have fun anyways");
	die();
	return 0;
}


