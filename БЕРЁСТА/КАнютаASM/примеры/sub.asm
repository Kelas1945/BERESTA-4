//**************************
// ������ ���� � �����������
// � ���� ������� 6
// � ����������� �� 1
//**************************

mov buf, 7 //����� 7 � �����������
mov a, buf

//����� � 0 ������ ~1
mov buf, 0
mov adr, buf
mov buf, 1
mov ram, buf

//����� � 8 ������ 1
mov buf, 8
mov adr, buf
mov buf, 1
mov ram, buf

gg:

mov buf, 0 //������������� ��������� �� ~1
mov adr, buf

sub p1
sub a

mov buf, 8 //������������� ��������� �� 1
mov adr, buf

mov ROMa1, loop
mov ROMa2, loop
je	//���� ����� �� ������� �� ����� loop

mov ROMa1, gg
mov ROMa2, gg
jmp 


loop:
mov ROMa1, loop
mov ROMa2, loop
jmp








