mov buf, 9  //����� � 9 ������ //
mov adr, buf
mov buf, 0 //���������� ���������� ���
mov r2, buf
mov buf, 10  //����� � 10 ������ //
mov adr, buf
mov buf, 4 //��� ���������
mov ram, buf
mov buf, 11  //����� � 11 ������ //
mov adr, buf
mov buf, 1 //��� �����+1
mov ram, buf
mov buf, 8 //� 8 ������ ������ �������
mov adr, buf
mov buf, 10 //����� ������� ����� �������� ��������������� �� ����
mov ram, buf
mov r1, buf 
mov buf, 0  //������� � ���� 0
mov p1, buf
start:
mov ram, r1
mov buf, 9  //������� 9 ������ //
mov adr, buf
mov a, ram //��������� � � ���������� ������
mov buf, 10  //������� 10 ������ //
mov adr, buf
mov roma1, end
mov roma2, end
je		//���� ����� �� ��������� 
mov buf, 11
mov adr, buf
add r1		//����������� ������� �� ������� � ��������� � r1
mov buf, 9  //������� 9 ������ //
mov adr, buf
mov ram, r1
mov buf, 8
mov adr, buf
mov a,ram
add r1
mov roma1, HIGH
mov roma2, HIGH
jc
//������ ������� � ����
mov buf,0
mov p1,buf
mov roma1, start
mov roma2, start
jmp 
//������� ������� � ����
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



















