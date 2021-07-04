import tkinter as tk
import threading
import numpy as np
import random
import threading
colors = ["blue","green","red","purple","#8f0e31","#0e966b","black","silver"]
matrix = np.full((14*18), 0)
pozicijeMine = [x for x in range(0,14*18)]
my_window = tk.Tk()
my_canvas = tk.Canvas(my_window, width=720,height=560,background="silver")
my_canvas.grid(row=0,column=0)
zastava = tk.PhotoImage(file="zastava.png")
naopaka = tk.PhotoImage(file="naopaka.png")
def drawCanvas():
    global netacneZastave
    netacneZastave = []
    for i in range(18):
        for j in range(14):
            my_canvas.create_rectangle(i*40, j*40, i*40+40, j*40+40, outline = 'black')
def MakeMatrix():
    for i in range(40):
        n = random.randint(0,len(pozicijeMine)-1)
        matrix[pozicijeMine[n]]=-1
        numbersAround = findAroundNumbers(pozicijeMine[n])
        pozicijeMine.pop(n)
        for okolina in numbersAround:
            if matrix[okolina]!=-1: matrix[okolina]+=1
def findAroundNumbers(poz):
    positions = []
    h = poz//18
    w = poz%18
    if((h-1)>=0):ImaGore=True
    else: ImaGore=False
    if((h+1)<=13):ImaDole=True
    else: ImaDole=False
    if((w-1)>=0):ImaLevo=True
    else: ImaLevo=False
    if((w+1)<=17):ImaDesno=True
    else: ImaDesno=False
    if ImaGore==True: positions.append(poz-18)
    if ImaDole==True: positions.append(poz+18)
    if ImaLevo==True: positions.append(poz-1)
    if ImaDesno==True: positions.append(poz+1) 
    if(ImaGore==True and ImaDesno==True): positions.append(poz-17)
    if(ImaGore==True and ImaLevo==True):positions.append(poz-19)
    if(ImaDole==True and ImaLevo==True):positions.append(poz+17)
    if(ImaDole==True and ImaDesno==True):positions.append(poz+19)
    return positions
drawCanvas()
MakeMatrix()
def kliknuo(e):
    h=e.y//40
    w=e.x//40
    if(matrix[h*18+w]==-1):
        print(netacneZastave)
        my_canvas.unbind("<Button-1>")
        my_canvas.unbind("<Button-3>")
        my_canvas.create_rectangle(w*40, h*40, w*40+40, h*40+40,fill='white',outline = 'black')
        my_canvas.create_oval(w*40+5,h*40+5,w*40+40-5,h*40+40-5,fill='black')
        global pozicijeMine
        global interval
        pozicijeMine = [x for x in range(14*18) if matrix[x]==-1]
        interval=threading.Timer(0.3, prikazatiMine)
        interval.start()                    
    elif(matrix[h*18+w]==0):
        pronadjiNule(h,w)
    elif(matrix[h*18+w]>0 and matrix[h*18+w]<9):
        my_canvas.create_rectangle(w*40, h*40, w*40+40, h*40+40,fill='white',outline = 'silver')
        boja=colors[matrix[h*18+w]-1]
        my_canvas.create_text(w*40+20,h*40+20,anchor="center",font="Purisa",fill=boja,text=matrix[h*18+w])
        matrix[h*18+w]=28
def pronadjiNule(h,w):
    poz = h*18+w
    if(matrix[poz]==0):
        my_canvas.create_rectangle(w*40, h*40, w*40+40, h*40+40,fill='white',outline = 'silver')
        matrix[poz]=28
        okolnaMesta = findAroundNumbers(poz)
        for mesto in okolnaMesta:
            pronadjiNule(mesto//18,mesto%18)
    else:
        if(matrix[h*18+w]!=28):
            my_canvas.create_rectangle(w*40, h*40, w*40+40, h*40+40,fill='white',outline = 'silver')
            boja=colors[matrix[h*18+w]-1]
            my_canvas.create_text(w*40+20,h*40+20,anchor="center",font="Purisa",fill=boja,text=matrix[h*18+w])
            matrix[h*18+w]=28
            
def desnoKliknuo(e):
    h=e.y//40
    w=e.x//40
    if matrix[h*18+w]!=28:
        if matrix[h*18+w]<10:
            if(matrix[h*18+w]!=-1):
                netacneZastave.append(h*18+w)
            my_canvas.create_image(w*40+20,h*40+20, anchor="center", image=zastava)
            my_canvas.create_rectangle(w*40, h*40, w*40+40, h*40+40,outline = 'black')
            matrix[h*18+w]=matrix[h*18+w]+12
        else:
            if h*18+w in netacneZastave:
                netacneZastave.pop(netacneZastave.index(h*18+w))
            my_canvas.create_rectangle(w*40, h*40, w*40+40, h*40+40,fill='silver',outline = 'black')
            matrix[h*18+w]=matrix[h*18+w]-12
def prikazatiMine():
    if len(pozicijeMine)!=0:
        h = pozicijeMine[0]//18
        w=pozicijeMine[0]%18
        my_canvas.create_rectangle(w*40, h*40, w*40+40, h*40+40,fill='white',outline = 'black')
        my_canvas.create_oval(w*40+5,h*40+5,w*40+40-5,h*40+40-5,fill='black')
        pozicijeMine.pop(0)
        interval=threading.Timer(0.3, prikazatiMine)
        interval.start()
    else:
        interval=threading.Timer(0.3, PrikazatiNaopakeZastave)
        interval.start()
def PrikazatiNaopakeZastave():
    if(len(netacneZastave)!=0):
        h=netacneZastave[0]//18
        w=netacneZastave[0]%18
        my_canvas.create_rectangle(w*40, h*40, w*40+40, h*40+40,fill='silver',outline = 'black')
        my_canvas.create_image(w*40+20,h*40+20, anchor="center", image=naopaka)
        netacneZastave.pop(0)
        interval=threading.Timer(0.3, PrikazatiNaopakeZastave)
        interval.start()
my_canvas.bind("<Button-1>", kliknuo)
my_canvas.bind("<Button-3>", desnoKliknuo)
my_canvas.focus_set()
my_canvas.pack()
my_canvas.mainloop()










