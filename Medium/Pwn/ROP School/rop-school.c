#include <stdio.h>
#include <signal.h>
#include <stdlib.h>
#include <errno.h>
#include <capstone/capstone.h>

#define CAPSTONE_ARCH CS_ARCH_X86
#define CAPSTONE_MODE CS_MODE_64
#define ul unsigned long
#define l long

/**
 * print_gadget() and print_chain() are adapted from kanak#0087 and pwn college's original function. 
 * Huge thanks to them for their original function and inspiration for this challenge. 
 */

void print_gadget(ul *gadget_addr)
{
  csh handle;
  cs_insn *insn;
  size_t count;
  unsigned char vec[64];

  if (cs_open(CAPSTONE_ARCH, CAPSTONE_MODE, &handle) != CS_ERR_OK) {
    printf("ERROR: disassembler failed to initialize.\n");
    return;
  }

  printf("| 0x%016lx: ", (ul)gadget_addr);

  int r = mincore((void *) ((uintptr_t)gadget_addr & ~0xfff), 64, vec);
  if (r < 0 && errno == ENOMEM) {
    printf("(UNMAPPED MEMORY)");
  }
  else {
    count = cs_disasm(handle, (void *)gadget_addr, 64, (uint64_t)gadget_addr, 0, &insn);
    if (count > 0) {
      for (size_t j = 0; j < count; j++) {
        printf("%s %s ; ", insn[j].mnemonic, insn[j].op_str);
        if (strcmp(insn[j].mnemonic, "ret") == 0 || strcmp(insn[j].mnemonic, "call") == 0) break;
      }

      cs_free(insn, count);
    }
    else {
      printf("(DISASSEMBLY ERROR) ");
      for (int k = 0; k < 16; k++) printf("%02hhx ", ((uint8_t*)gadget_addr)[k]);
    }
  }
  printf("\n");

  cs_close(&handle);
}

void print_chain(ul **chain_addr, int chain_length)
{
  printf("\n+--- Printing %ld gadgets of ROP chain at %p.\n", chain_length, chain_addr);
  for (int i = 0; i < chain_length; i++) {
    print_gadget(*(chain_addr + i));
  }
  printf("\n");
}

void timeout(int signum) {
    printf("Timeout!");
    exit(-1);
}

ul rp;
unsigned int readaddr;

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    signal(SIGALRM, timeout);
    alarm(60);
}

void win(int user_id, int passcode){
	if (user_id==0x1337 && passcode==0x31337){
			printf("Welcome Admin\n");
			system("/bin/bash");
	}
	else{
		printf("Try harder smh my head\n");
		printf("Current User ID: %d, Expected: %d\n", user_id,0x1337);
		printf("Current Passcode: %d, Expected: %d\n",passcode, 0x31337);

		exit(-1);
	}
}

int main() {
    setup();
    char buf[32];
    rp = &buf[40];
    printf("Welcome to ROP School\n");
    printf("In this challenge, we have a win function located at %p.\n",win);
    printf("To get the flag, you need to call the win() function.\n\n");
    printf("As you should have learnt from Buffer Overflow School previously,\n");
    printf("We call a function by directly overflowing into the return address.\n");
    printf("The return address is stored at %p, %d bytes after the start of your input buffer.\n",rp,(l)(rp)-(l)(buf));
    printf("That means that you will need to input at least %d bytes.\n",rp + (8 - (long)buf));
    printf("Of which you will need to fill the buffer of size %d,\n",32);
    printf("%d to fill other stuff stored between the buffer and the return address (thanks GCC),\n",rp + (-32 - (long)buf));
    puts("And 8 bytes that will overwrite the return address.\n\n");
    printf("Your Input: \n");
    readaddr = read(0,buf,4096);
    printf("Received %d bytes! Potentially %d gadgets. \n",readaddr,(ul)(buf + ((int)readaddr-rp))>>3);
    print_chain(rp,(int)((ul)(buf + ((int)readaddr-rp))>>3));
    printf("ROP disassembler exiting! \n");
    return 0;

}

