from tkinter import *
import connection as con
from PIL import Image,ImageTk
from tkinter import messagebox as mbox

rev_u =0
def rev_u_window(lis,log_id,n):
    global rev_u
    add = str(n)+'.jpg'
    state = con.check_rev_u(log_id,lis.get('name'))
    # making tkinter window
    rev_u =Toplevel()
    rev_u.geometry('700x400+100+70')
    rev_u.title("REVIEW")

    #making main frame
    main_frame= Frame(rev_u,bg='black')

    #making canvas that contain product review
    prod_frame = Canvas(main_frame,scrollregion=(0,0,1000,1000))

    #making scrollbar
    scrollbar = Scrollbar(main_frame, command=prod_frame.yview,orient='vertical')
    prod_frame.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT,fill='y')

    #making window which contain the review
    rev_frame= Frame(prod_frame,bg='#131d20')
    #____________________________________________________
    back = Image.open("Back_but.jpg")
    back = back.resize((120, 30), Image.ANTIALIAS)
    back = ImageTk.PhotoImage(back)
    bak = Button(prod_frame, image=back, command=lambda: [rev_u.destroy()])
    bak.image = back
    prod_frame.create_window(2, 0, window=bak, anchor="nw",tag='back')

    #______________________________________________________________________________

    #making frame which contain product information
    info_frame = Frame(rev_frame,bg='#131d20')

    #___________________________________
    pr = Image.open(add)
    pr = pr.resize((70, 65), Image.ANTIALIAS)
    pr = ImageTk.PhotoImage(pr)
    #_____________________________________

    #_____________________________________________________________________________________________________________
    #making product information
    lab = Label(info_frame,image=pr)
    lab.image = pr  # this is anchor image object to label
    lab.config(image=pr)
    lanam = Label(info_frame, text=lis.get("name"), fg="white", wraplength=600, bg='#131d20',font="Arial 10 bold")
    laprice = Label(info_frame, text=lis.get("price"), fg="white", bg='#131d20',font="Arial 13 bold")
    laadd = Label(info_frame, text=lis.get("address"), fg="white", bg='#131d20',font="Arial 10 ")
    lab.grid(row=0,column=0,rowspan=2,padx=5)
    lanam.grid(row=0,column=1,columnspan=3)
    laprice.grid(row=1,column=2)
    laadd.grid(row=1,column=3)
    #_____________________________________________________________________________________________________________

    info_frame.pack(side=TOP,fill='x',padx=5)
    lis_of_rev =con.fetch_rev_u(lis.get("name"))
    #print(lis_of_rev)
    frames =[]
    for i in range(0,len(lis_of_rev)):
        inside_rev_frame = Frame(rev_frame,bg='#131d20')
        frames.append(inside_rev_frame)
        i+=1
    prof = Image.open('profile.png')
    prof = prof.resize((20, 20), Image.ANTIALIAS)
    prof = ImageTk.PhotoImage(prof)

    for j in range(0,len(lis_of_rev)):
        try:
            pic = Label(frames[j],image=prof)
            pic.image=prof
            name = Label(frames[j],text=lis_of_rev[j].get('name'),font='Arial 12 bold', fg="white", bg='#131d20')
            star = Label(frames[j],text=lis_of_rev[j].get('star')*'\u2B50',font='Arial 12 bold', fg="white", bg='#131d20')
            date = Label(frames[j],text=lis_of_rev[j].get('date'),font='Arial 12 ', fg="white", bg='#131d20')
            rev = Label(frames[j],text=lis_of_rev[j].get('review'),font='Arial 10', fg="white", bg='#131d20')

            pic.grid(row=0,column=0,padx=4)
            name.grid(row=0,column=1)
            star.grid(row=1,column=2)
            date.grid(row=2,column=0)
            rev.grid(row =3,column=0,columnspan=3)
            frames[j].pack(side=TOP,padx=5)
            j+=1

        except:
            print("Error")

    # ________________________________________________________
    im = Image.open('resize.png')
    im = im.resize((700, 350), Image.ANTIALIAS)
    im = ImageTk.PhotoImage(im)
    # _________________________________________________________
    # making background image
    prod_frame.create_image(0, 0, image=im, anchor="nw")
    # creating window that show product review
    window = prod_frame.create_window(2, 40, window=rev_frame, anchor="nw",tag='rev_frame')

    # adjusting frame inside canvas
    prod_frame.configure(scrollregion=prod_frame.bbox("all"))
    rev_u.bind('<Configure>',lambda event:prod_frame.itemconfig(window, width=prod_frame.winfo_width()-7))

    prod_frame.pack(fill=BOTH,expand=1)

    #making text frame for taking review
    if state == True:

        text_frame = Frame(main_frame)

        text = Text(text_frame,width=300,height=10,font="Arial 10 bold",bg='#131d20',fg='white',insertbackground='white')
        new_frame = Frame(text_frame,bg='#131d20')

        in_label = Label(new_frame,text="Number of "+'\u2B50',font="Arial 10 bold",bg='#131d20',fg='white')
        lbox = Listbox(new_frame,height=5,width=20,font="Arial 10 bold",bg='#131d20',fg='white')
        send = Button(new_frame,text='send',font="Arial 12 bold",bg='white'
                      ,command=lambda : [insert_in(log_id,lbox,text,lis.get("name"),send,rev_frame)])
        for i in range(1,6):
            lbox.insert(END,str(i)+'.'+i*'\u2B50')
        in_label.pack(side=TOP)
        lbox.pack()
        send.pack(fill='x')
        new_frame.pack(side=RIGHT,fill='y')
        text.pack(side=TOP)

        text_frame.pack(side=BOTTOM,fill='x',expand=1)


    main_frame.pack(side=TOP, fill=BOTH,expand=1)

    rev_u.mainloop()


def insert_in(log_id,lbox,text,pr_name,btn,rev_frame):
    global rev_u
    if lbox.curselection()==():
        mbox.showinfo("Message", "Please select Number of Stars")
        rev_u.deiconify()
        return
    elif text.compare("end-1c", "==", "1.0"):
        mbox.showinfo("Message", "Please Write review")
        rev_u.deiconify()
        return

    #print(text.get('1.0',END))
    #print(lbox.curselection())
    #print(pr_name)
    response = mbox.askquestion("Send response", "Send this review")
    if response=='yes':
        con.addrev_u(log_id,text.get('1.0',END),pr_name,(lbox.curselection()[0]+1))
        prof = Image.open('profile.png')
        prof = prof.resize((20, 20), Image.ANTIALIAS)
        prof = ImageTk.PhotoImage(prof)
        frame = Frame(rev_frame,bg='#131d20')
        pic = Label(frame, image=prof)
        pic.image = prof
        name = Label(frame, text='You', font='Arial 12 bold', fg="white", bg='#131d20')
        star = Label(frame, text=(lbox.curselection()[0]+1) * '\u2B50', font='Arial 12 bold', fg="white",
                     bg='#131d20')
        date = Label(frame, text='Now', font='Arial 12 ', fg="white", bg='#131d20')
        rev = Label(frame, text=text.get('1.0',END), font='Arial 10', fg="white", bg='#131d20')

        pic.grid(row=0, column=0, padx=4)
        name.grid(row=0, column=1)
        star.grid(row=1, column=2)
        date.grid(row=2, column=0)
        rev.grid(row=3, column=0, columnspan=3)
        frame.pack(side=TOP,padx=5)
        btn.destroy()
        text.config(state="disabled")

    rev_u.deiconify()
    return




#lis = con.fetchpod('kayub4947@gmail.com')
#print(lis)
#rev_u_window(lis,'kayub4947@gmail.com')