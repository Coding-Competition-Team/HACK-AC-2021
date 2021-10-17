#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
#install pwntools with pip if you haven't already by now

#p = process('./bof.o') #use this when testing your exploit offline. Rename buf.o to your binary
p = remote("URL", PORT) # change URL to given URL and port to given port


p.recvuntil("<some text in your program>") #specify until where pwntools should receive too
#i.e to say, recvuntil() tells pwntools to receive text until the text u specified
#replace <some text in your program> with the actual text

#to receive an address, use the following code
addr = int(p.recvuntil(""),16) #where you change where pwntools should receive until
#combining both lines of code above will effectively tell pwntools the address is between the end of the first specified received until up till the start of the second recvuntil

#to send something, you can use p.sendline(). For example, 
p.sendline(b"A"*3) #would send AAA and a newline

#to deal withh python3 byte wrangling issues, one can define a buffer as such
buffer = b"A"*100 #notice the letter b which is used to tell python to treat this as bytes
#This is also seen above where the letter b is used in p.sendline()

#to encode addresses or data (like your binary's function address) in little endian format, make use of p64() or p32(). 
#note that p64() should be used for 64-bit programs. i.e to say, p64() should be used for data types of size 8 bytes (like long long or function addresses)
#for example
p64(win) #this encodes win in little endian format


#p32() should be used for 32-bit programs. i.e to say, p32() should be used for data types of size 4 bytes (like integers)
#for example
p32(0xdeadbeef) #this encodes 0xdeadbeef as a 4 byte little endian format


#to switch to interactive mode, use 
p.interactive()






