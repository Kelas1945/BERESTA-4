//**********************
// пример счета до 7
// с записью в порт
//**********************
mov buf,0
mov a, buf

gg:

mov buf,8
mov adr, buf

mov buf,1
mov ram,buf

add p1
add a

mov buf, 7
mov ram,buf

mov ROMa1, loop
mov ROMa2, loop
je	//если равны то переход

mov ROMa1, gg
mov ROMa2, gg
jmp


loop:
mov ROMa1, loop
mov ROMa2, loop
jmp










