mov buf, 9  //пишем в 9 €чейку //
mov adr, buf
mov buf, 0 //количество переданных бит
mov r2, buf
mov buf, 10  //пишем в 10 €чейку //
mov adr, buf
mov buf, 4 //дл€ сравнени€
mov ram, buf
mov buf, 11  //пишем в 11 €чейку //
mov adr, buf
mov buf, 1 //дл€ счета+1
mov ram, buf
mov buf, 8 //в 8 €чейку пам€ти запишем
mov adr, buf
mov buf, 10 //число которое нужно передать последовательно по биту
mov ram, buf
mov r1, buf 
mov buf, 0  //выводим в порт 0
mov p1, buf
start:
mov ram, r1
mov buf, 9  //покажем 9 €чейку //
mov adr, buf
mov a, ram //переносим в ј содержимое €чейки
mov buf, 10  //покажем 10 €чейку //
mov adr, buf
mov roma1, end
mov roma2, end
je		//если равно то закончить 
mov buf, 11
mov adr, buf
add r1		//увеличиваем счетчик на единицу и сохран€ем в r1
mov buf, 9  //покажем 9 €чейку //
mov adr, buf
mov ram, r1
mov buf, 8
mov adr, buf
mov a,ram
add r1
mov roma1, HIGH
mov roma2, HIGH
jc
//низкий уровень в порт
mov buf,0
mov p1,buf
mov roma1, start
mov roma2, start
jmp 
//высокий уровень в порт
HIGH:
mov buf,1	
mov p1, buf
mov roma1, start
mov roma2, start
jmp 

end:

mov buf, 0
mov p1, buf
mov roma1,end
mov roma2,end
jmp



















