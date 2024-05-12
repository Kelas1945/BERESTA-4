from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox 

from PIL import ImageChops
from PIL import Image

from PIL import ImageTk
from tkinter.ttk import Progressbar
from tkinter import filedialog
from tkinter import filedialog as fd

import serial #установка pip install pyserial
import time
import binascii
from time import sleep

import tkinter as tk
import tkinter.messagebox as mb
from tkinter.messagebox import showinfo, askyesno
from tkinter.messagebox import askyesnocancel
from tkinter import ttk

import matplotlib.pyplot as plt


def insertText(): #открыть программы для микрохи
    file_name = fd.askopenfilename(filetypes=(("ассемблер", "*.asm"),("All files", "*.*")))
    lb29.configure (text=file_name)
    
    if file_name!="":
        text.delete(0.0, END)
        text.tag_config('lable', background="yellow", foreground="red")
        text.tag_config('reg', foreground="blue")
        text.tag_config('kom', foreground="green")
        with open(file_name, encoding="cp1251") as f:
            s = f.readline()
            while s:
               
                s1=s.strip()
                result=s1.partition(':')
                if (result[1]!=''):                
                    text.insert(END, s1, 'lable')
                    text.insert(END, "\n")
                else:
                    sep2='//'
                    result2=s.partition(sep2)

                    if result2[1]==sep2:
                        text.insert(END, result2[0])
                        text.insert(END, result2[1], 'kom')
                        text.insert(END, result2[2], 'kom')
                    else:
                        text.insert(END, s)
                        
                        
                s = f.readline()
        f.close()    
    
         
def extractText(): #сохранить программу
    global new_project
    global modified
    modified=0
    
    file_name = fd.asksaveasfilename(filetypes=(("ассемблер", "*.asm"),("All files", "*.*") ))
    if file_name!="":
        lb29.configure (text=file_name)
        result3=file_name.partition('.asm')
        if (result3[1]!='.asm'):
            file_name=file_name+".asm"

        f = open(file_name, 'w')
        s = text.get(1.0, END)
        f.write(s)
        f.close()
    
        new_project=1
    else : new_project=0        

    
def clicked4(): #компиляция
    global realport
    global portActiv
    global stroki
    global step_step
    global step_step2
    global labelsRAM
    global wavform
    global wavform2
    global wavform3
    global wavform4
    global wavform_st

    
## ************ статические инструкции ****

    instruction = {
        'mov a buf': 0x05,
        'mov a p2': 0x25,
        'mov a r1': 0x35,
        'mov a ram': 0x45,
        'mov a r2': 0x55,
        
        'mov adr buf': 0x06,
        'mov adr p2': 0x26,
        'mov adr r1': 0x36,
        'mov adr r2': 0x56, 
        'mov ram buf': 0x07,
        'mov ram p2': 0x27,
        'mov ram r1': 0x37,
        'mov ram r2': 0x57, 
        'mov p1 buf': 0x08,
        'mov p1 p2': 0x28,
        'mov p1 r1': 0x38,
        'mov p1 ram': 0x48,
        'mov p1 r2': 0x58, 
        'mov r1 p2': 0x29,
        'mov r1 buf': 0x09,
        'mov r1 ram': 0x49,
        'mov r1 r2': 0x59,

        
        'mov r2 buf': 0x00,
        'mov r2 p2': 0x20,
        'mov r2 r1': 0x30,
        'mov r2 ram': 0x40,
        

        'add adr': 0x16,
        #'add ram': 0x17,
        'add p1': 0x18,
        'add a': 0x15,
        'add r1': 0x19,
        'add r2': 0x10,

        'sub adr': 0x96,
        #'sub ram': 0x97,
        'sub p1': 0x98,
        'sub a': 0x95,
        'sub r1': 0x99,
        'sub r2': 0x90,        
             
        
        'jmp': 0x03,
        'je': 0x13,
        'jc': 0x23,
        'jbz0': 0x43,
        'jbz1': 0x53,
        'jbz2': 0x63,
        'jbz3': 0x73,
         
    }
    
    k155ru2()
    
    metka=""
    error=""
    adres=0
    intege=""
    lab=""

    step_step=0
    step_step2=0

    error_next=0
    
    lb4.configure (text="")
    kod.delete(0.0, END)
    
    mas = []
    lable = []
    lable_sp=[]
    lable_oper=[]
    
    integ =[]
    binarik=[]
    st_l=0
    f=0

    prg=[]

    del wavform[:] #очистить данные для диаграммы
    del wavform2[:] #очистить данные для диаграммы
    del wavform3[:] #очистить данные для диаграммы
    del wavform4[:] #очистить данные для диаграммы
    wavform_st=0


#сбрасываем все регисты
    BUF.configure (text=str(hex(0)))
    A.configure (text=str(hex(0)))
    R1.configure (text=str(hex(0)))
    R2.configure (text=str(hex(0)))
    P1.configure (text=str(hex(0)))
    ADR.configure (text=str(hex(0)))
    ROMA1.configure (text=str(hex(0)))
    ROMA2.configure (text=str(hex(0)))

   
    for i in range(16):
        if i<8: labelsRAM[i].configure (text=str(hex(15)))
        else: labelsRAM[i].configure (text=str(hex(0)))
    
    
    s = text.get(1.0, END).splitlines()
    for line in s:
        stroka=line.lower()
        stroka=stroka.strip() #убрать пробелы в начале и конце
        #убрать пустые строки
        if stroka!="":
    #убрать коментарии
            result=stroka.partition('//')
            if (result[1]!=''):
                stroka=result[0]
                
        if stroka!="":
    #убрать коментарии
            prg.append([])
            prg[adres]=stroka
            adres=adres+1            

#собрать названия всех меток        
        result=stroka.partition(':')
        if (result[1]!=''):
            metka=result[0]
            metka=metka.strip() #убрать пробелы в начале и конце
            metka=" ".join(metka.split()) #убрать повторяющиеся пробелы
            for i in range(len(lable_sp)):
                if lable_sp[i]==metka: messagebox.showerror('Ошибка', 'дубликат метки <'+metka+'>')
                
            lable_sp.append([])
            lable_sp[st_l]=metka
            st_l=st_l+1
            if (result[2]!=''): messagebox.showerror('Ошибка', 'отделите метку <'+stroka+'> от команды')
                

    adres=0
    metka=""

##    for i in range(len(prg)):
##        
##        print (prg[i])
        
        
    for ii in range(len(prg)):
        stroka=prg[ii].lower()
        stroka=stroka.strip() #убрать пробелы в начале и конце
    
        result=stroka.partition(':')
        if (result[1]!=''):
           
            metka=result[0]
            metka=metka.replace(","," ") #заменить запятую на пробел
            metka=metka.strip() #убрать пробелы в начале и конце
            metka=" ".join(metka.split()) #убрать повторяющиеся пробелы
       
               
        else:
            if stroka!="":

                stroka=stroka.strip() #убрать пробелы в начале и конце
                stroka=" ".join(stroka.split()) #убрать повторяющиеся пробелы
                result=stroka.partition(',')
                intege=""
                res2=result[2].strip() #убрать пробелы в начале и конце
                res0=result[0].strip() #убрать пробелы в начале и конце
                if (res2.isdigit()):
                    stroka=res0
                    intege=res2
                else:
                    for i in range(len(lable_sp)):
                        #print (lable_sp[i])
                        if lable_sp[i]==res2:
                            stroka=res0
                            lab=res2
                            f=1
                    if f==0:
                        stroka=res0+" "+res2
                        lab=""
                    f=0        
                    intege="";

                mas.append([])
                lable.append([])
                integ.append([])
                lable_oper.append([])
                stroka=stroka.strip() #убрать пробелы в начале и конце
                mas[adres]=stroka
                lable[adres]=metka
                integ[adres]=intege
                lable_oper[adres]=lab
                adres=adres+1
            metka=""
            

    print ("*** обработка ***")


    adres=0
    for i in range(len(mas)):
        unit=mas[i]
        if unit in instruction:
            data = instruction[unit]
            binarik.append([])
            binarik[adres]=data
            adres=adres+1
        else:
            #обработка отсутствия значения в словаре
            if unit=='mov buf':
                data=int(integ[i])
                data=data<<4
                data=data+4
                binarik.append([])
                binarik[adres]=data
                adres=adres+1
            else:
                error=1
                if unit== 'mov roma1':
                    for j in range(len(lable)):
                        if lable[j]==lable_oper[i]:
                            data=j&0x0F
                            data=data<<4
                            data=data+1
                            binarik.append([])
                            binarik[adres]=data
                            adres=adres+1
                            error=0
                            

                else:
                    if unit== 'mov roma2':
                        for j in range(len(lable)):
                            if lable[j]==lable_oper[i]:
                                data=j&0xF0
                                data=data+2
                                binarik.append([])
                                binarik[adres]=data
                                adres=adres+1
                                error=0
                if error==1:
                        
                        if error_next==0: messagebox.showerror('Информация', 'ошибка в <'+unit+','+integ[i]+lable_oper[i]+'> строке ')
                        error_next+=1
                        lb4.configure (text="ошибок = "+str(error_next)+" шт.")
                        

    for i in range(len(binarik)):
        result=hex(binarik[i])
        kod.insert(END,result+'\n')
    print ("*** готово ***")
    lbx.configure (text=str(len(binarik)))

    
    

########################################################
    f = open('CodeForFlash\com.bin', 'wb')

    s = kod.get(1.0, END).splitlines()
    lbx.configure (text=str(len(s)-1))
    for line in s:
        if line!='':
            i=int(line,16)
            f.write(bytes(chr(i), 'iso8859-1'))
    f.close()
                 

def clickk():
    global new_project
    result =  askyesnocancel(title="", message="СОХРАНИТЬСЯ?")
    if result==None: new_project=0
    elif result:
        extractText()
    else : new_project=1
    
def newText():
    global new_project
    global modified     
    new_project=0   
    if modified==0:
        lb29.configure (text="")
        text.delete(0.0, END)
        kod.delete(0.0, END)
    else:        
        clickk()
        if new_project==1:
            lb29.configure (text="")
            text.delete(0.0, END)
            kod.delete(0.0, END)
            modified=0
              
def info():
    messagebox.showinfo('Информация', 'Компилятор для ЭВМ Берёста (и только для её!!!).\n cpurus@yandex.ru\n Попов Н.П.\n 2024 ')

def read_reg():
    global pb1
    global pb2
    global Flag
    global Aa
    global ADRus
    global ramsik
    global Aaa
    global AaaSUB

    adstrok=ADR.cget("text")
    ADRus=int(adstrok.partition('x')[2],16)
    
    ramsik = labelsRAM[ADRus].cget("text")
    ramsik= ramsik.partition('x')[2]
    
    Aa=A.cget("text")
    Aa= Aa.partition('x')[2]
    Aaa=int(ramsik,16)+int(Aa,16)
    AaaSUB=int(Aa,16)+int(ramsik,16)
        
    Flag=Aaa&0x10
    Flag=Flag>>4
    
    Aaa=Aaa&0x0F
    AaaSUB=AaaSUB+1
    AaaSUB=AaaSUB&0x0F


def steps():
    global step_step
    global step_step2
    global labelsRAM
    global labelsADR
    
    global pb1
    global pb2
    global Flag
    global Aa
    global ADRus
    global ramsik
    global Aaa
    global AaaSUB

    global wavform
    global wavform2
    global wavform3
    global wavform4
    global wavform_st
        

#берем содержимое входного порта
    P2_in=0 
    P2_in=enabled3.get()<<1
    P2_in=P2_in+enabled2.get()<<1
    P2_in=P2_in+enabled1.get()<<1
    P2_in=P2_in+enabled0.get() #P2_in = полубайт порта

       
    kod.tag_config('lable', background="yellow", foreground="red")   
    s = kod.get(1.0, END).splitlines()
    #print (len(s))
    if step_step<len(s)-1:
        stroka=s[step_step2].lower()
        kod.replace(str(step_step2+1)+".0", str(step_step2+1)+"."+str(len(stroka)), stroka)
       
        stroka=s[step_step].lower()
        kod.replace(str(step_step+1)+".0", str(step_step+1)+"."+str(len(stroka)), stroka,'lable')
        step_step2=step_step

        strokus=stroka.partition('x')[2]
        pb1=int(strokus,16)&0x0F
        pb2=int(strokus,16)&0xF0
        pb2=pb2>>4

        
        read_reg()

        labelsADR[ADRus].configure (text=labelsADR[ADRus].cget("text"),background="white")

        #регистры=P2
        if (pb2==2)&(pb1==5): A.configure (text=str(hex(P2_in)))
        if (pb2==2)&(pb1==6): ADR.configure (text=str(hex(P2_in)))
        if (pb2==2)&(pb1==8): P1.configure (text=str(hex(P2_in)))
        if (pb2==2)&(pb1==9): R1.configure (text=str(hex(P2_in)))
        if (pb2==2)&(pb1==0): R2.configure (text=str(hex(P2_in)))
        
        if (pb2==2)&(pb1==7):
            if ADRus>7:
                labelsRAM[ADRus].configure (text=str(hex(P2_in)))
            else:
                
                strokus3=P2_in
                strokus3=~strokus3
                strokus3=strokus3&0x0f
                labelsRAM[ADRus].configure (text=str(hex(strokus3)))                
        

        
        #BUF=число
        if pb1==4: BUF.configure (text=str(hex(pb2)))
        if pb1==1: ROMA1.configure (text=str(hex(pb2)))
        if pb1==2: ROMA2.configure (text=str(hex(pb2)))

        

        #регистры=BUF
        if (pb2==0)&(pb1==5): A.configure (text=BUF.cget("text"))
        if (pb2==0)&(pb1==9): R1.configure (text=BUF.cget("text"))
        if (pb2==0)&(pb1==8): P1.configure (text=BUF.cget("text"))
        if (pb2==0)&(pb1==0): R2.configure (text=BUF.cget("text"))
        if (pb2==0)&(pb1==6): ADR.configure (text=BUF.cget("text"))
        if (pb2==0)&(pb1==7):
            if ADRus>7:
                labelsRAM[ADRus].configure (text=BUF.cget("text"))
            else:
                strokus2=BUF.cget("text").partition('x')[2]
                strokus3=int(strokus2,16)
                strokus3=~strokus3
                strokus3=strokus3&0x0f
                labelsRAM[ADRus].configure (text=str(hex(strokus3)))

        #регистры=R1
        if (pb2==3)&(pb1==5): A.configure (text=R1.cget("text"))
        if (pb2==3)&(pb1==6): ADR.configure (text=R1.cget("text"))
        if (pb2==3)&(pb1==8): P1.configure (text=R1.cget("text"))
        if (pb2==3)&(pb1==0): R2.configure (text=R1.cget("text"))
        if (pb2==3)&(pb1==7):        
            if ADRus>7:
                labelsRAM[ADRus].configure (text=R1.cget("text"))
            else:
                strokus2=R1.cget("text").partition('x')[2]
                strokus3=int(strokus2,16)
                strokus3=~strokus3
                strokus3=strokus3&0x0f
                labelsRAM[ADRus].configure (text=str(hex(strokus3)))

        

        #регистры=R2
        if (pb2==5)&(pb1==5): A.configure (text=R2.cget("text"))
        if (pb2==5)&(pb1==6): ADR.configure (text=R2.cget("text"))
        if (pb2==5)&(pb1==8): P1.configure (text=R2.cget("text"))
        if (pb2==5)&(pb1==9): R1.configure (text=R2.cget("text"))
        if (pb2==5)&(pb1==7):
            if ADRus>7:
                labelsRAM[ADRus].configure (text=R2.cget("text"))
            else:
                strokus2=R2.cget("text").partition('x')[2]
                strokus3=int(strokus2,16)
                strokus3=~strokus3
                strokus3=strokus3&0x0f
                labelsRAM[ADRus].configure (text=str(hex(strokus3)))



        #регистры=ОЗУ
        if (pb2==4)&(pb1==5): A.configure (text=str(hex(int(ramsik,16))))
        if (pb2==4)&(pb1==8): P1.configure (text=str(hex(int(ramsik,16))))
        if (pb2==4)&(pb1==9): R1.configure (text=str(hex(int(ramsik,16))))
        if (pb2==4)&(pb1==0): R2.configure (text=str(hex(int(ramsik,16))))

        #регистры=АЛУ+
        if (pb2==1)&(pb1==5): A.configure (text=str(hex(Aaa)))
        if (pb2==1)&(pb1==6): ADR.configure (text=str(hex(Aaa)))
        if (pb2==1)&(pb1==8): P1.configure (text=str(hex(Aaa)))
        if (pb2==1)&(pb1==9): R1.configure (text=str(hex(Aaa)))
        if (pb2==1)&(pb1==0): R2.configure (text=str(hex(Aaa)))

        #регистры=АЛУ-
        if (pb2==9)&(pb1==5): A.configure (text=str(hex(AaaSUB)))
        if (pb2==9)&(pb1==6): ADR.configure (text=str(hex(AaaSUB)))
        if (pb2==9)&(pb1==8): P1.configure (text=str(hex(AaaSUB)))
        if (pb2==9)&(pb1==9): R1.configure (text=str(hex(AaaSUB)))
        if (pb2==9)&(pb1==0): R2.configure (text=str(hex(AaaSUB)))


            
        ST.configure (text=str(step_step))

        read_reg()
        
        if Flag: FlagL.configure (text="True", fg='#0aff0a')
        else: FlagL.configure (text="False", fg='#ff0a0a')

        if int(ramsik,16)==int(Aa,16): FlagLZ.configure (text="True", fg='#0aff0a')
        else: FlagLZ.configure (text="False", fg='#ff0a0a')

        labelsADR[ADRus].configure (text=labelsADR[ADRus].cget("text"),background="yellow")                                   
        
        step_step=step_step+1

        ROMad2=ROMA2.cget("text")
        ROMadd2=ROMad2.partition('x')[2]
        ROMtmp=int(ROMadd2,16)
        ROMtmp=ROMtmp<<4
        ROMad1=ROMA1.cget("text")
        ROMadd1=ROMad1.partition('x')[2]
        ROMtmp=ROMtmp+int(ROMadd1,16)
        
        #jmp
        if (pb2==0)&(pb1==3):
            step_step=ROMtmp
            
        #je    
        if (pb2==1)&(pb1==3):
            if FlagLZ.cget("text")=="True":
                step_step=ROMtmp
                
        #'jc': 0x23,
        if (pb2==2)&(pb1==3):
            if FlagL.cget("text")=="True":
                step_step=ROMtmp

##        'jbz0': 0x43,
##        'jbz1': 0x53,
##        'jbz2': 0x63,
##        'jbz3': 0x73, 
        bitA=A.cget("text")
        bitA=bitA.partition('x')[2]
       
        if (pb2==4)&(pb1==3)&(int(bitA,16)==1): step_step=ROMtmp
        if (pb2==5)&(pb1==3)&(int(bitA,16)==2): step_step=ROMtmp
        if (pb2==6)&(pb1==3)&(int(bitA,16)==4): step_step=ROMtmp
        if (pb2==7)&(pb1==3)&(int(bitA,16)==8): step_step=ROMtmp



        P1_wav_t=P1.cget("text")
        P1_wav=P1_wav_t.partition('x')[2]
        P1_wav_int=int(P1_wav,16)& 1
        P1_wav_int2=int(P1_wav,16)& 2
        if P1_wav_int2==2: P1_wav_int2=3
        else: P1_wav_int2=2
        P1_wav_int3=int(P1_wav,16)& 4
        if P1_wav_int3==4: P1_wav_int3=5
        else: P1_wav_int3=4
        P1_wav_int4=int(P1_wav,16)& 8
        if P1_wav_int4==8: P1_wav_int4=7
        else: P1_wav_int4=6
        
        wavform.append([])#данные для графика
        wavform[wavform_st]=P1_wav_int
        
        wavform2.append([])#данные для графика
        wavform2[wavform_st]=P1_wav_int2

        wavform3.append([])#данные для графика
        wavform3[wavform_st]=P1_wav_int3

        wavform4.append([])#данные для графика
        wavform4[wavform_st]=P1_wav_int4
        
        wavform_st=wavform_st+1


            
def on_closing():
    global modified
    if modified==1:
        if messagebox.askyesno("выход", "сохраниться?"):
            extractText()
    root.destroy()

def on_modified(event):
    global modified
    modified=1

def plot_port():
    global wavform
    global wavform2
    global wavform3
    global wavform4
    plot, axes = plt.subplots(num="диаграмма порта P1")
    plt.plot(wavform)
    plt.plot(wavform2)
    plt.plot(wavform3)
    plt.plot(wavform4)
    plt.text(0, 6, "3", fontsize=15)
    plt.text(0, 4, "2", fontsize=15)
    plt.text(0, 2, "1", fontsize=15)
    plt.text(0, 0, "0", fontsize=15)
    plt.show()


def starts():
    a=0
    
    if entry.get().isdigit():
        step = int(entry.get())
        while a < step:
            a = a+1
            steps()
    else: messagebox.showerror('Информация', 'неверное количество итераций <'+entry.get()+'>')

def k155ru2 ():
    global labelsRAM
    global labelsADR
    
    string='ADR'
    nums=['0','1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
    labelsADR =[]
    labelsRAM =[]

    for x in nums:
        jk=string+x
        if int(x)<8: adr=tk.Label(frame4,text=jk, font=("Arial Bold", 15), fg='#0aafaf',background="white")
        else: adr=tk.Label(frame4,text=jk, font=("Arial Bold", 15), fg='#0a0aff',background="white")
        adr.grid(column=0, row=int(x))
        labelsADR.append(adr)

        if int(x)<8: ram=tk.Label(frame4,text=str(hex(15)), font=("Arial Bold", 15))
        else: ram=tk.Label(frame4,text=str(hex(0)), font=("Arial Bold", 15))
        ram.grid(column=1, row=int(x))
        labelsRAM.append(ram)

####################################################################
global ff
global ee4
global modified
global step_step
global step_step2
global labelsRAM

global wavform
global wavform2
global wavform3
global wavform4
global wavform_st

global labelsRAM


wavform_st=0

wavform=[]
wavform2=[]
wavform3=[]
wavform4=[]

step_step=0
step_step2=0


modified=0


ff=0


root = Tk()
root.iconbitmap(r'img\logo.ico')
root.title("КАнюта 1.0")  
root.geometry('1100x650+100+0')
root.resizable(False, False)


#root.overrideredirect(1) #полноэкранный режим
#root.state('zoomed')

frame1=Frame(root, bd=1, relief=RAISED)
frame1.pack(side=TOP, fill=X)

frame7=Frame(root, bd=1, relief=RAISED)
frame7.pack(side=TOP, fill=X)


frame9=Frame(root, bd=1, relief=RAISED) 
frame9.pack(side=BOTTOM, fill=Y)

frame2=Frame(root, bd=1, relief=RAISED)
frame2.pack(side=LEFT, fill=Y)

frame6=Frame(root, bd=1, relief=RAISED)
frame6.pack(side=RIGHT,fill=Y)

frame3=Frame(root, bd=1, relief=RAISED)
frame3.pack(side=RIGHT,fill=Y)

frame4=Frame(root, bd=1, relief=RAISED)
frame4.pack(side=RIGHT,fill=Y)

frame5=Frame(root, bd=1, relief=RAISED)
frame5.pack(side=RIGHT,fill=Y)



mainmenu = Menu(frame1) 
root.config(menu=mainmenu)

filemenu = Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Новый",command=newText)
filemenu.add_command(label="Открыть",command=insertText)
filemenu.add_command(label="Сохранить",command=extractText)
filemenu.add_command(label="Выход",command=on_closing)
 
helpmenu = Menu(mainmenu, tearoff=0)
helpmenu.add_command(label="О программе", command=info)
 
mainmenu.add_cascade(label="Файл", menu=filemenu)
mainmenu.add_cascade(label="Справка", menu=helpmenu)



lb29 = Label(frame7, text="", font=("Arial Bold", 10))  #название открытого файла
lb29.pack(side=LEFT, fill=X)

btn3 = Button(frame1, text="Компилировать", command=clicked4)  
btn3.grid(column=5, row=0, padx=5)

message = StringVar()
message.set("100")
entry = tk.Entry(frame1, fg="black", bg="white", width=5, textvariable=message)
entry.grid(column=6, row=0, padx=5)

start = Button(frame1, text="старт", command=starts)  
start.grid(column=7, row=0, padx=5)

step = Button(frame1, text="1 шаг", command=steps)  
step.grid(column=8, row=0, padx=5)


plott = Button(frame1, text="диаграммы P1", command=plot_port)  
plott.grid(column=10, row=0, padx=5)



lbx = Label(frame7, text="0", font=("Arial Bold", 15), fg='#0aff0a')
lbx.pack(side=RIGHT, fill=X)
lb3 = Label(frame7, text="размер бинарника", font=("Arial Bold", 15))
lb3.pack(side=RIGHT, fill=X)

#метка для ошибок
lb4 = Label(frame7, text="", font=("Arial Bold", 15), fg='#ff0a0a')  
lb4.pack(side=LEFT, fill=X)


#текст программы
text = Text(frame2, width=71, height=33, wrap=WORD)
text.pack(side=LEFT, fill=Y)
scroll = Scrollbar(frame2,command=text.yview)
scroll.pack(side=LEFT, fill=Y)
text.config(yscrollcommand=scroll.set)
text.bind("<KeyRelease>", on_modified)

#код программы
kod = Text(frame2, width=4, height=33, wrap=WORD)
kod.pack(side=LEFT, fill=Y)
scroll1 = Scrollbar(frame2,command=kod.yview)
scroll1.pack(side=LEFT, fill=Y)
kod.config(yscrollcommand=scroll1.set)

k155ru2()

ROMA1a=Label(frame4,text="ROMa1", font=("Arial Bold", 15), fg='#0afa0f')
ROMA1a.grid(column=0, row=17)
ROMA1=Label(frame4,text=str(hex(0)), font=("Arial Bold", 15))
ROMA1.grid(column=1, row=17)

ROMA2a=Label(frame4,text="ROMa2", font=("Arial Bold", 15), fg='#0afa0f')
ROMA2a.grid(column=0, row=18)
ROMA2=Label(frame4,text=str(hex(0)), font=("Arial Bold", 15))
ROMA2.grid(column=1, row=18)

    
BUFa = Label(frame3, text="BUF", font=("Arial Bold", 15), fg='#0aff0a')
BUFa.grid(column=1, row=0)
BUF = tk.Label(frame3, text=str(hex(0)), font=("Arial Bold", 15))
BUF.grid(column=2, row=0)

Aa = Label(frame3, text="A", font=("Arial Bold", 15), fg='#ff0aff')
Aa.grid(column=1, row=1)
A = tk.Label(frame3, text=str(hex(0)), font=("Arial Bold", 15))
A.grid(column=2, row=1)

R1a = Label(frame3, text="R1", font=("Arial Bold", 15), fg='#0a0aff')
R1a.grid(column=1, row=2)
R1 = tk.Label(frame3, text=str(hex(0)), font=("Arial Bold", 15))
R1.grid(column=2, row=2)

R2a = Label(frame3, text="R2", font=("Arial Bold", 15), fg='#0a0aff')
R2a.grid(column=1, row=3)
R2 = tk.Label(frame3, text=str(hex(0)), font=("Arial Bold", 15))
R2.grid(column=2, row=3)

P1a = Label(frame3, text="P1", font=("Arial Bold", 15), fg='#0abfbf')
P1a.grid(column=1, row=4)
P1 = Label(frame3, text=str(hex(0)), font=("Arial Bold", 15))
P1.grid(column=2, row=4)

ADa = Label(frame3, text="ADR", font=("Arial Bold", 15), fg='#0abfbf')
ADa.grid(column=1, row=9, pady=20)
ADR = tk.Label(frame3, text=str(hex(0)), font=("Arial Bold", 15))
ADR.grid(column=2, row=9, pady=20)

Flaga = Label(frame3, text="CF", font=("Arial Bold", 15), fg='#aabbbf')
Flaga.grid(column=1, row=10)
FlagL = tk.Label(frame3, text='False', font=("Arial Bold", 15), fg='#ff0a0a')
FlagL.grid(column=2, row=10)

Flagb = Label(frame3, text="ZF", font=("Arial Bold", 15), fg='#aabbbf')
Flagb.grid(column=1, row=11)
FlagLZ = tk.Label(frame3, text='False', font=("Arial Bold", 15), fg='#ff0a0a')
FlagLZ.grid(column=2, row=11)



STa=Label(frame5,text="ST", font=("Arial Bold", 15), fg='#0afa0f')
STa.grid(column=0, row=0)
ST=Label(frame5,text="0", font=("Arial Bold", 15))
ST.grid(column=0, row=1)


STa=Label(frame6,text="P2", font=("Arial Bold", 15), fg='#0afa0f')
STa.grid(column=0, row=0)

enabled3 = IntVar()  
enabled_checkbutton3 = ttk.Checkbutton(frame6, variable=enabled3)
enabled_checkbutton3.grid(column=1, row=1)
enabled2 = IntVar()  
enabled_checkbutton2 = ttk.Checkbutton(frame6, variable=enabled2)
enabled_checkbutton2.grid(column=2, row=1)
enabled1 = IntVar()  
enabled_checkbutton1 = ttk.Checkbutton(frame6, variable=enabled1)
enabled_checkbutton1.grid(column=3, row=1)
enabled0 = IntVar()  
enabled_checkbutton0 = ttk.Checkbutton(frame6, variable=enabled0)
enabled_checkbutton0.grid(column=4, row=1)

STa=Label(frame6,text="3")
STa.grid(column=1, row=2)
STa=Label(frame6,text="2")
STa.grid(column=2, row=2)
STa=Label(frame6,text="1")
STa.grid(column=3, row=2)
STa=Label(frame6,text="0")
STa.grid(column=4, row=2)


root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
