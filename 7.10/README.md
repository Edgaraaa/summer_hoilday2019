# 7.10 

*今天主要是刷了一个web的基础题库，毕竟是学校无聊培训期间。索性就玩玩*

## 第0关

你就输入```真实姓名```就进入第1关了

## 第1关

​	第1关看起来像个登陆界面，然后我们点击试试发现用户名点不了，之后密码可以点，所以右击查看源码

![](https://github.com/Edgaraaa/summer_hoilday2019/blob/master/7.10/img/1.png?raw=true)

之后看到底下```js```的代码，好的```password```就是```passwordissimple```

## 第2关

​	老套路第一件事查源码

![](https://github.com/Edgaraaa/summer_hoilday2019/blob/master/7.10/img/2.png?raw=true)

发现没啥东西可看，也不能干等啊，我们输入试试看，我账号密码同样输入```111```得到了```SELECT ID FROM admin WHERE user = '111' AND pass = '111'```我们发现是个注入题而且没有啥过滤，直接万能密码一把梭啊。账号密码同样```' or '1'='1```

# 第3关

又是输入密码，看源码

```html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3c.org/TR/1999/REC-html401-19991224/loose.dtd">
<HTML dir=ltr lang=zh-CN xmlns="http://www.w3.org/1999/xhtml">
<HEAD>
<TITLE>评估业务大比武第3关</TITLE>
<META http-equiv="Content-Type" content="text/html; charset=UTF-8">
<LINK id=login-css rel=stylesheet type=text/css href="css/login.css" media=all>
<LINK id=colors-fresh-css rel=stylesheet type=text/css href="css/color.css" media=all>
<META name=robots content=noindex,nofollow>
<META name=GENERATOR content="MSHTML 8.00.6001.19170"></HEAD>
<BODY class=login>
<DIV id=login>
<script type="text/javascript" src="passishere"></script>
<FORM id=loginform method=post name=loginform action=l3check.php>
<P><LABEL>密码<BR><INPUT id=user_pass class=input tabIndex=20 type=password name=pwd></LABEL> </P>
<P class=submit><INPUT tabIndex=10 value=登陆 onclick="check(pwd.value)"></P></FORM>
</DIV>
<p id="backtoblog"><a href="index.php" title="不知道自己在哪？"><b>欢迎来到<font color=red>第3关</font></b></a></p>
</BODY></HTML>
<script type="text/javascript">
<!--
function check(pwd) {
if (pwd==PASSWORD){
	alert("Good!\n欢迎来到第4关 ...");
	location.href = CORRECTSITE;
	}
else {
	alert("OMG!\n你确定？ ...");
    location.href = WRONGSITE;
	}
	PASSWORD="AbCdExx";
	CORRECTSITE="l4ierdddca.php";
	WRONGSITE="http://www.google.com";
	//-->
}
</script>
```

发现了熟悉的```js```代码，但是不对劲啊，咋会有```HTML```的注释符号啊，那就不看了啊，再好好看了看代码，发现了某文件```js```引用啊。```<script type="text/javascript" src="passishere"></script>```，我点开看了看好的吧，密码给你了。```DieHard```

## 第4关

​	还是密码啊，老套路

```html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3c.org/TR/1999/REC-html401-19991224/loose.dtd">
<HTML dir=ltr lang=zh-CN xmlns="http://www.w3.org/1999/xhtml">
<HEAD>
<TITLE>评估业务大比武第4关</TITLE>
<META http-equiv="Content-Type" content="text/html; charset=UTF-8">
<LINK id=login-css rel=stylesheet type=text/css href="css/login.css" media=all>
<LINK id=colors-fresh-css rel=stylesheet type=text/css href="css/color.css" media=all>
<META name=robots content=noindex,nofollow>
<META name=GENERATOR content="MSHTML 8.00.6001.19170"></HEAD>
<BODY class=login>
<DIV id=login>
<FORM id=loginform method=post name=loginform action=l4cxaaxwq2.php>
<P><LABEL>密码<BR><INPUT id=user_pass class=input tabIndex=20 type=password name=pwd></LABEL> </P>
<!--hash=md5(password)，hash='3396ec84858608b7fb98de830f9b23ae'，password=？-->
<P class=submit><INPUT type=submit tabIndex=10 value=登陆></P></FORM>
</DIV>
<p id="backtoblog"><a href="#" title="不知道自己在哪？"><b>欢迎来到<font color=red>第4关</font></b></a></p>
</BODY></HTML>
```

定睛一看，一条奇怪的注释，那就不说了md5搜起来，得到```20140410```就是密码。

> 我用的md5搜索网站:[https://www.somd5.com/](https://www.somd5.com/)

## 第5关

​	这题给了一个文档```pass.doc```，做的时候以为是CTF杂项题(别说真的是杂项题)，以为```hex```码看一波就能出答案但是吧，他还就是个纯暴力破解题，我也是纯的无奈了。我用了这个软件*PassFab Word Password Recovery*(网上有破解版)，跑出来密码是```word```（这题我真的不知道出题人思路），之后打开```word```文档之后看到的是一串```base64```*"d2VsY29tZXRvanhjYQ=="*，之后译码之后得到的是```welcometojxca```（这题很莫名其妙）

## 第6关

​	这题正式和抓包扯上关系了，我们先看源码，一如既往的没有东西，之后试着输入一些东西。得到了一句话```**当前登录用户权限为user;而非admin**，2秒后自动跳转到上一页面```。明显的啊，就是一个抓包改权限，

![](https://github.com/Edgaraaa/summer_hoilday2019/blob/master/7.10/img/3.png?raw=true)

之后看到有个```level=user```，试着改成```admin```，竟然真的过了。

## 第7关

​	这个一看就知道到也是抓包了，之后改一个```user-agrnt```就可以了，

![](https://github.com/Edgaraaa/summer_hoilday2019/blob/master/7.10/img/4.png?raw=true)

改成```IE13```就可以了，之后到下半部分，之后开始看源码，发现又是一个奇怪的注释，还是md5，

```html
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3c.org/TR/1999/REC-html401-19991224/loose.dtd">
<HTML dir=ltr lang=zh-CN xmlns="http://www.w3.org/1999/xhtml">
<HEAD>
<TITLE>评估业务大比武第7关</TITLE>
<META http-equiv="Content-Type" content="text/html; charset=UTF-8">
<LINK id=login-css rel=stylesheet type=text/css href="css/login.css" media=all>
<LINK id=colors-fresh-css rel=stylesheet type=text/css href="css/color.css" media=all>
<META name=robots content=noindex,nofollow>
<META name=GENERATOR content="MSHTML 8.00.6001.19170"></HEAD>
<BODY class=login>
<DIV id=login>
<FORM id=loginform method=post name=loginform action=l7cplsx112.php>
<P><LABEL>密码<BR><INPUT id=user_pass class=input tabIndex=20 type=password name=pwd></LABEL> </P><P class=submit><INPUT type=submit tabIndex=10 value=登陆></P><!--加密方式:md5(md5($password).$salt)，hash='eb5056e6607152fc916b2c54ca13a5e1'，$salt='123456'，$password=？，可以用到的工具passwordspro，密码长度为4位小写字母--></FORM>
</DIV>
<p id="backtoblog"><a href="#" title="不知道自己在哪？"><b>欢迎来到第7关  <font color=red><b>恭喜，即将接近成功！</b></font></a></p>
</BODY></HTML>
```

之后还是用刚刚的网站，直接就可以搜到，还加盐md5，搜就完事。```jxca```

## 第8关

​	文件上传？莫非要传木马，然后骑马，驾驾驾~~，但是我试着上传了一个小东西，发现给提示了

***允许上传图片，请绕过验证上传一个JSP文件**。4秒后自动返回*，奥，文件类型绕过，二话不说还是抓包，莫非是抓包抓上瘾了，(我其实以为要传php木马，但是是个jsp)，随便创建一个后缀为```jsp```的文件，然后上传抓包。

```http
POST /l8cogijssss.php HTTP/1.1
Host: 192.168.223.128
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Referer: http://192.168.223.128/l8iopaxsa231.php
Content-Type: multipart/form-data; boundary=---------------------------2908129352731
Content-Length: 333
Connection: close
Cookie: hibext_instdsigdipv2=1; PHPSESSID=8l1spr1lujkmrk8pprsh1ij3e0; user=%E7%9C%9F%E5%AE%9E%E5%A7%93%E5%90%8D; level=user
Upgrade-Insecure-Requests: 1

-----------------------------2908129352731
Content-Disposition: form-data; name="file"; filename="hello.jsp"
Content-Type: application/octet-stream

xxxxxxxxxx
-----------------------------2908129352731
Content-Disposition: form-data; name="submit"

Submit
-----------------------------2908129352731--
```

之后看到了一个```content-type```这个东西，好像是和自己上传的文件类型有关啊(百度就能查到)，那能上传照片？好啊，那我改一下类型不就完了(因为是post包上传)，改成```image/jpeg```完事。

得到了

```
File Name: hello.jsp
File Type: image/jpeg
File Size: 0.0302734375 Kb
Temp File: C:\wamp\tmp\php1B.tmp
level 9 http://3.3.3.5/l9idcc7opp.php
```

这也就是最后一关的开始啊。

## 第9关 也就是最后一关

​	给的提示看了看好像就是最后的一个```url```和第九关有关系啊，那我就进去看看，发现不对劲。```3.3.3.5```这个```ip```不对劲啊，应该是改成本地服务器的地址吧，于是乎就把访问的php文件复制过去了，

```纳尼？居然是错的？嗯，就是错的```，woc个mmp，之后想了想原来如此，那个```3.3.3.5```应该就是我要蜜汁访问的网站吧，没错还是抓包。

```http
GET /l9idcc7opp.php HTTP/1.1
Host: 192.168.223.128
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: close
Cookie: hibext_instdsigdipv2=1; PHPSESSID=8l1spr1lujkmrk8pprsh1ij3e0; user=%E7%9C%9F%E5%AE%9E%E5%A7%93%E5%90%8D; level=user
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0
```

把```Host```设置成```3.3.3.5```应该就是这个样子吧。

之后又是一个蜜汁密码框，还有一只从头到尾的蜜汁老虎

![](https://github.com/Edgaraaa/summer_hoilday2019/blob/master/7.10/img/5.gif?raw=true)

之后还是看源码

```html
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3c.org/TR/1999/REC-html401-19991224/loose.dtd">
<HTML dir=ltr lang=zh-CN xmlns="http://www.w3.org/1999/xhtml">
<HEAD>
<TITLE>第9关，最后一关</TITLE>
<META http-equiv="Content-Type" content="text/html; charset=UTF-8">
<LINK id=login-css rel=stylesheet type=text/css href="css/login.css" media=all>
<LINK id=colors-fresh-css rel=stylesheet type=text/css href="css/color.css" media=all>
<META name=robots content=noindex,nofollow>
<META name=GENERATOR content="MSHTML 8.00.6001.19170"></HEAD>
<BODY class=login>
<DIV id=login><h1><a href="//////l9chhh00ss.txt" title='般若菠萝蜜！芝麻开门！玛尼玛尼哄！'></a></h1>
<FORM id=loginform method=post name=loginform action=l9chhh00ss.php>
<P><LABEL>密码<BR><INPUT id=user_pass class=input tabIndex=20 type=password name=pwd></LABEL> </P>
<P class=submit><INPUT type=submit tabIndex=10 value=登陆></P></FORM>
</DIV>
<p id="backtoblog"><a href="#" title="不知道自己在哪？"><b>欢迎来到<font color=red>第9关</font>，最后一关啦！</b></a></p>
</BODY></HTML>
```

发现没啥好玩的啊，咋想也不对啊，之后看到一个引用不对劲，点看瞅瞅也没东西啊，因为给的那个路径不对劲啊，我就猜就是他当前目录，没错源代码泄露

```php
<?
$pass = $_POST['pwd'];
if (encrypt($pass)=="uxnuxnkz2295x9x") {
	header('Location: '.$pass.'.php');
}

function encrypt($str)
{
        $encrypt_key = 'abcdefghijklmnopqrstuvwxyz1234567890';
        $decrypt_key = 'ngzqtcobmuhelkpdawxfyivrsj2468021359';

        if (strlen($str) == 0) return false;

        for ($i=0; $i<strlen($str); $i++){
                for ($j=0; $j<strlen($encrypt_key); $j++){
                        if ($str[$i] == $encrypt_key[$j]){
                                $enstr .= $decrypt_key[$j];
                                break;
                        }
                }
        }

        return $enstr;
}
?>
```

之后一看代码审计啊，明显逆向题倒过来写啊，啥也别说直接用C

我们可以根据上面的代码写出判断php本地测试一下

```php
<?php
$pass = "jsajsanc1109s0s";
if(encrypt($pass)=="uxnuxnkz2295x9x"){
	echo "1";
}
else {
	echo "0";
}
	

function encrypt($str)
{
        $encrypt_key = 'abcdefghijklmnopqrstuvwxyz1234567890';
        $decrypt_key = 'ngzqtcobmuhelkpdawxfyivrsj2468021359';
        $enstr='';
        if (strlen($str) == 0) return false;

        for ($i=0; $i<strlen($str); $i++){
                for ($j=0; $j<strlen($encrypt_key); $j++){
                        if ($str[$i] == $encrypt_key[$j]){
                                $enstr .= $decrypt_key[$j];
                                break;
                        }
                }
        }

        return $enstr;
}
?>
```

之后根据这个写出C代码

```c
#include <iostream>
#include <cstring>
using namespace std;
char epass[] = "uxnuxnkz2295x9x";
char ekey[] = "abcdefghijklmnopqrstuvwxyz1234567890";
char dkey[] = "ngzqtcobmuhelkpdawxfyivrsj2468021359";
char sp[100];
void decrypt()
{
	int kkp = 0;
	for (int i = 0; i < strlen(epass); i++)
	{
		for (int j = 0; j < strlen(dkey); j++)
		{
			if (epass[i] == dkey[j])
			{
				sp[kkp] = ekey[j];
				kkp++;
				break;
			}
		}
	}
	cout << sp << endl;
}
int main()
{
	decrypt();
	return 0;
}
```

答案已经在判断脚本里面了。

```jsajsanc1109s0s```

## 九关闯完的感受

​	说句实话没有一点滋味，挺适合入门用的一个题库，之后就是基本前端代码审计挺无聊的，适合入门。

