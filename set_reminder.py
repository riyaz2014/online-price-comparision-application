from tkinter import *
import connection as con
from PIL import Image,ImageTk
from tkinter import messagebox as mbox
import os

time_format='Hr'

rem = 0
def reminder_window(dic,log_id):

    global rem
    #___________________
    rem = Toplevel()
    rem.geometry('400x130+100+70')
    rem.title("REMINDER")

    info = Frame(rem,bg='black')
    add = os.path.join("wishlist", str(dic.get('name') + ".jpg"))
    #-----------------------------------------------
    im = Image.open(add)
    im = im.resize((70, 65),Image.ANTIALIAS)
    im = ImageTk.PhotoImage(im)
    #-------------------------------------------------

    prod = Label(info,image=im)
    prod.image=im
    nam = Label(info, text=dic.get("name"), fg="white", wraplength=600, bg='#131d20', font="Arial 10 bold")
    price = Label(info, text=dic.get("price"), fg="white", bg='#131d20', font="Arial 13 bold")
    add = Label(info, text=dic.get("address"), fg="white", bg='#131d20', font="Arial 10 ")
    prod.grid(row=0, column=0, rowspan=2, padx=5)
    nam.grid(row=0, column=1, columnspan=3)
    price.grid(row=1, column=2)
    add.grid(row=1, column=3)
    info.pack(fill='x')

    input_frame = Frame(rem)
    check = Label(input_frame,text="Check After Every :",font="Arial 13 bold")
    time = Entry(input_frame,width=4,font="Arial 11 bold")
    time_btn = Menubutton(input_frame,text="Hr ",font="Arial 11 bold",activebackground='yellow')
    menu = Menu(time_btn,tearoff=0)
    menu.add_command(label="Hr",command=lambda :[time_btn.config(text="Hr "),set_format("Hr")])
    menu.add_command(label="Min", command=lambda: [time_btn.config(text="Min "), set_format("Min")])
    time_btn['menu']=menu

    check.pack(side=LEFT)
    time.pack(side=LEFT)
    time_btn.pack(side=LEFT)
    input_frame.pack(fill='x')

    buttn_frame = Frame(rem)
    set_btn =Button(buttn_frame,text=u"\u23f0"+"set Reminder",font="Arial 11 bold",fg="white", bg='#131d20'
                    ,width=23,command=lambda : set_rminder(dic.get('name'),log_id,time.get(),time_format))
    cancel = Button(buttn_frame,text='Cancel',font="Arial 11 bold",fg="white", bg='#131d20',
                    width=20 ,command=lambda :rem.destroy())
    set_btn.pack(side=LEFT)
    cancel.pack(side=LEFT)

    buttn_frame.pack(fill='x')
    rem.mainloop()


def set_format(f):
    global time_format
    time_format = f


def set_rminder(name,log_id,time,tm_format):
    global rem
    if time =='':
        mbox.showinfo("Message", "Please Enter time input")
        rem.deiconify()
    elif time.isdigit():
        con.addrem(name,log_id, time+tm_format)
        mbox.showinfo("Message", "reminder set for every "+time+' '+tm_format)
        rem.deiconify()
    else :
        mbox.showinfo("Message", "Please Enter correct time input")
        rem.deiconify()

#dic = {'name':'Redmi Note 10 Shadow Black 6GB+128GB','price':"100000",'address':'Mi.com'}
#reminder_window(dic,'kayub4947@gmail.com')

