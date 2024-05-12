//**************************
// пример кода с вычитаниием
// в порт пишется 6
// и уменьшается до 1
//**************************

mov buf, 7 //пишем 7 в аккумулятор
mov a, buf

//пишем в 0 ячейку ~1
mov buf, 0
mov adr, buf
mov buf, 1
mov ram, buf

//пишем в 8 ячейку 1
mov buf, 8
mov adr, buf
mov buf, 1
mov ram, buf

gg:

mov buf, 0 //устанавливаем указатель на ~1
mov adr, buf

sub p1
sub a

mov buf, 8 //устанавливаем указатель на 1
mov adr, buf

mov ROMa1, loop
mov ROMa2, loop
je	//если равны то переход на метку loop

mov ROMa1, gg
mov ROMa2, gg
jmp 


loop:
mov ROMa1, loop
mov ROMa2, loop
jmp








