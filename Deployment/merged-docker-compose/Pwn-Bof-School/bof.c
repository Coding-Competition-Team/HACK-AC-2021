#include <stdio.h>
#include <signal.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

#define arr_size 0x18
#define overflow_size 0x10
#define canary 0x8
#define total (arr_size+overflow_size+canary)

/**
 * print_buffer() was adapted from NUS Greyhats Welcome CTF Challenge. https://github.com/NUSGreyhats/welcome-ctf-2021
 * Huge thanks to NUS Greyhats and Enigmatrix for the concept and inspiration for this challenge. 
 */

//prints out the buffer!
void print_buffer(char* buffer) {
    for (int i = 0; i < total * 3 + 4; i++) printf("-");
    printf("\n");
    printf("%-71s | %-23s | %-23s | %-23s \n", "Contents", "Stack Canary", "Saved Base ptr", "Return Address");
    for (int i = 0; i < total * 3 + 4; i++) printf("-");
    printf("\n");
    //print buffer
    for (int i = 0; i < arr_size; i++) {
        printf("%02x ", (buffer[i] & 0xff));
    }
    printf("| ");
    //print Stack Canary
    for (int i = arr_size; i < arr_size + 8; i++) {
        printf("%02x ", (buffer[i] & 0xff));
    }
    printf("| ");
    //print Saved Base Pointer
    for (int i = arr_size+8; i < arr_size + 16; i++) {
        printf("%02x ", (buffer[i] & 0xff));
    }
    printf("| ");
    //print Return addr
    for (int i = arr_size+16; i < arr_size + 24; i++) {
        printf("%02x ", (buffer[i] & 0xff));
    }
    printf("\n");
    for (int i = 0; i < total * 3 + 4; i++) printf("-");
    printf("\n");
}

void vuln() {
    char buffer[arr_size];
    memset(buffer, 0, arr_size);

    while(1) {
        printf("Input:\n");
        fgets(buffer, (total+5), stdin);
        print_buffer(buffer);
        printf("\nStack Canary\t\t: %p\nsaved base pointer\t: %p\nreturn address\t\t: %p\n", *((long*)(buffer + arr_size )), *((long*)(buffer + arr_size + 8)),*((long*)(buffer + arr_size + 16)));
        printf("Retry? (Y/N) If you have already overwritten the return address, please enter 'N'.\nYour Input: ");
        
        //newline handling
        char buf[10];
        fgets(buf, 10, stdin);
        char again;
        sscanf(buf, "%c", &again);
        if (again == 'N')
            break;
    }
}

void win() {
    system("/bin/sh");
}

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

int main() { 
    setup();
    printf("=== Buffer Overflow School ===\n");
    printf("Enter your input in, and it'll print it back in hexdump format. And maybe you could even get a flag :D\n");
    printf("Well unlike other buffer overflows, we have included a Stack Canary to protect this program...\n");
    printf("You could think of the stack canary as a 8 byte value below the array, which the program will compare with the original stack canary\n");
    printf("It is essential that the stack canary value is the same as the original stack canary. If not, our program would crash! \n");
    printf("Hint, addresses and the stack canary need to be converted to little endian format. Refer to the exploit template!\n");
    printf("Btw, there is an inaccessible function at %p (win). Maybe you can buffer overflow and win???\n\n", (win+1));
    
    vuln();
    return 0;
}
