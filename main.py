from tkinter import *
from PIL import Image,ImageTk
from PIL import ImageEnhance
import webScarpper as wb
import webbrowser as google
import traceback
import os
import voice_search as vs
import cv2 as cv
import shutil as sh
import connection as con
from tkinter import messagebox as mbox
import set_review as sr
import set_reminder as srem

#--------------------------global function----------------------------------#
#log_id
log_id = ''
#global list to store all searches
lis_of_sear = []

#global list to store all the links of website
lis_of_link = []

#global list to hold wish list product later we will use sql
lis_of_wish = []

#global variable of none type
dt = None

# call func for main result frame of searches
def call(name):
    lis_of_sear.append(name)
    global dt
    if dt is not None:

        #destroy previous search
        dt.detr()

    # take result list from getlis and call search result frame
    dt = product(t, getlis(name))

# use to visit website
# call by visit site button
def visit_link(i):

    #open the website in default Browser
    google.open_new(lis_of_link[i])

#deleting all images
def freeup():
    for i in range(0,7):
        try:
            os.remove(str(i)+".jpg")
        except:
            break

#make Dynamic Button
def mkButton(p,frame):
    return Button(frame, text="Visit site",font=("times new roman ",8,"bold")
                  ,activebackground="yellow", command=lambda: visit_link(p))
#make review button
def reviewbtn(i,frame,dic):
    return Button(frame, text="Reviews", font=("times new roman ", 8, "bold")
                  , activebackground="yellow", command=lambda: sr.rev_u_window(dic,log_id,i))

#make reminder button
def rembutton(p,frame,lis):
    return Button(frame, text=u"\u23f0"+"set Reminder", font=("times new roman ", 8, "bold")
               ,activebackground='yellow' , command=lambda:[set(lis[p],log_id)])
#to set reminder
def set(dic,log_id):
    srem.reminder_window(dic,log_id)

    pass
#get list of the product
def getlis(na):

   try:
       #making object of web scraping
        wa = wb.webScrapper()
        try:

            #delete the image from directory
            wa.delete()

        except:
            print(" ")

        link = wa.get(na)
        lis = wa.scrapgog(link["Google"])
        wa.download()

        if type(lis)==None:
            raise EXCEPTION("NOT THERE")
        return lis

   except ConnectionResetError as c:
       return "NOT CONNECTED"

   except :
       return "NOT FOUND"

# function for forward or backward search
def for_back(command,name,obj):

    global dt
    global back_count
    global forward_count

    if command == "back" and dt is not None:
        if (lis_of_sear.index(name)-1) < 0:
            return
        dt.detr()
        try:
            pr = lis_of_sear[lis_of_sear.index(name)-1]

        except :
            pr = lis_of_sear[0]

        obj.putinSearch(pr)

        try:
            dt = product(t,getlis(pr))

        finally:
            return

    if command == "forward" and dt is not None:
        if (lis_of_sear.index(name)+1) >= len(lis_of_sear):
            return
        dt.detr()
        pr = lis_of_sear[lis_of_sear.index(name)+1]
        obj.putinSearch(pr)
        try:

            dt = product(t, getlis(pr))
        finally:
            return
    if command=="search":
        try:
            pr = lis_of_sear[-1]
            dt = product(t, getlis(pr))
        finally:
            return

    return

#making image button
def imagebutton(frame,i):
    return Button(frame,command=lambda :[show(i)])

#showing image in pop up window
def show(i):
    #print(.jpg")
    #image = Image.open(str(i)+".jpg")
    #cimg = cv.CreateImageHeader(image.size, cv.IPL_DEPTH_8U, 3)  # CV Image
    img = cv.imread(str(i)+".jpg",1)
    res = cv.resize(img, (170, 250))
    #dst = cv.edgePreservingFilter(res, flags=1, sigma_s=60, sigma_r=0.4)
    dst = cv.detailEnhance(res, sigma_s=10, sigma_r=0.1)
    cv.namedWindow("Image")
    cv.moveWindow("Image",120,150)
    cv.imshow("Image",dst)
    cv.waitKey(0)
    cv.destroyAllWindows()

#voice function return take the search from microphone
def voice():
    v = vs.voice_search()
    return v.asist()

#to make wishlist window vivible
def wish(self):
    try:
        try:
            dt.detr()
        except:
            print(" ")
        self.scroll.pack_forget()
        wi = wishlist()
    except:
        print("")


def send_message(id,self):
    try:
        i = con.fetchpass(id)
        if i==1:
            raise EXCEPTION
        mbox.showinfo("Message", "Password send to your email_id")
        self.login(t, 9)
    except:
        mbox.showinfo("Message", "Email id entered is incorrect")


def contain_digit(txt):
    for x in txt:
        if x.isdigit():
            return True
    else:
        return False


def contain_alphabet(txt):
    for x in txt:
        if x.isalpha():
            return True
    else:
        return False


special_charater = ["@", "#", "$", "%", "&"]


def contain_special_charater(txt):
    for x in txt:
        if x in special_charater:
            return True
    else:
        return False


def set_signup(log_id,user_name,passwd):
    try:
        if "@gmail.com" not in log_id:
            mbox.showwarning(
                "Not Vaild E-mail id", "E-mail Address Entered is incorrect")
            return
        if len(passwd)< 8:
            mbox.showinfo("not valid password",
                                "password lenght should be more than or equal to 8")
            return
        elif not contain_special_charater(passwd):
            mbox.showinfo("not valid password",
                                "password does not contain special charater")
            return
        elif not contain_digit(passwd):
            mbox.showinfo("not valid password",
                                "password does not contain digit")
            return
        elif not contain_alphabet(passwd):
            mbox.showinfo("not valid password",
                                "password does not contain alphabet")
            return

        con.signup(user_name,log_id,passwd)
        setlogin(log_id)
        optionbar(t)
        mbox.showinfo("Welcome",
                      "TO SKAARS smart shopping")

    except:
        print("21")

def setlogin(log):
    global log_id
    log_id = log


def logout(obj):
    response = mbox.askquestion("Log Out","Do you really wnt to Log Out",icon="warning")
    if response == 'yes':
        global canvas
        obj.scroll.pack_forget()
        canvas.delete('all')
        canvas.pack_forget()
        first()
    else:
        return


        #------------------------------------class of frames--------------------------#


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

                                            # HEADER = LOGINPAGE

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

class header():
    # making a top frame
    def __init__(self, t):
        #giving tittle a
        t.title("SKARS Smart Shopping")
        # giving background black color
        t.configure(bg="#000000")
        #giving size to tk window
        t.geometry("990x550+20+70")

        self.login(t,bg)

#making login page
    def login(self,t,bg):

        # using global variable canvas in method
        global canvas

        # creating a login Frame
        self.bframe = Frame(t, relief="groove", bd=3)

        # resizing image use in button
        #--------------------------------------------------------------------#
        goog = Image.open("googlebut1.jpg")
        goog = goog.resize((250,50),Image.ANTIALIAS)
        goog = ImageTk.PhotoImage(goog)
        log = Image.open("login.jpg")
        log = log.resize((250, 50), Image.ANTIALIAS)
        log = ImageTk.PhotoImage(log)
        #--------------------------------------------------------------------#

        loginfr = Frame(self.bframe,bg="White",bd=0)
        head = Label(loginfr,text="LOGIN",font="Arial 20 bold")
        email = Label(loginfr,text="LOGIN ID:",font="Arial 12 bold")
        emid = Entry(loginfr, width=30,relief="groove",font="Arial 12 ",bd=2,justify=LEFT)
        paswd = Label(loginfr, text="PASSWORD:",font="Arial 12 bold",bd=2)
        password = Entry(loginfr, width=30,font="Arial 12 bold",relief="groove",bd=2,show="*")
        foget_pass  = Button(loginfr,text="Forget_password",bd=0,fg="blue",command=lambda :[loginfr.destroy(),self.update_pass()])
        #using image as button
        logbtn = Button(loginfr,image=log,bd=0
                       ,command=lambda:[self.enter(t,emid.get(),password.get())])
        logbtn.image = log  # -> anchor to image
        createbtn = Button(loginfr, image=goog,bd=0
                         ,command=lambda: [loginfr.destroy(),self.sign_up()])
        createbtn.image=goog # -> anchor to image

        # an Empty label to create space or to skip a line using pack
        space = Label(loginfr,text="")

        head.grid(row=0,column=1,columnspan=3,pady=4)
        space.grid(row=1)
        email.grid(row=2,column=2,sticky="w",pady=2,padx=2)
        emid.grid(row=3,column=2,sticky="ew",pady=2,padx=2)
        paswd.grid(row=4,column=2,sticky="w",pady=2,padx=2)
        password.grid(row=5,column=2,sticky="ew",pady=3,padx=2)
        foget_pass.grid(row=6,column=2,sticky='e')
        logbtn.grid(row=7,column=2,columnspan=3,pady=5)
        createbtn.grid(row=8,column=2,columnspan=3,pady=5)
        #adding keyboard listener
        #emid.bind('<Return>', lambda event=None:[password.icursor(0)])
        password.bind('<Return>', lambda event=None:[logbtn.invoke()])

        loginfr.pack(fill="y")

        #adding bframe  in canvas
        canvas.create_window(150,120, anchor="nw", window=self.bframe)

    def enter(self,t,e_id,passwd):
        # login Button will call this and destroy ist frame
        global log_id
        if con.login(e_id,passwd):
            log_id = e_id
            self.bframe.destroy(),
            optionbar(t)
        else :
            mbox.showinfo("Message", "Incorrect Password or email_id")

    def update_pass(self):

        # resizing image use in button
        # --------------------------------------------------------------------#
        sen = Image.open("send.jpg")
        sen = sen.resize((180, 40), Image.ANTIALIAS)
        sen = ImageTk.PhotoImage(sen)
        log = Image.open("Back_but.jpg")
        log = log.resize((140, 35), Image.ANTIALIAS)
        log = ImageTk.PhotoImage(log)
        # --------------------------------------------------------------------#

        #-----------------------------------------------  #
        loginforget = Frame(self.bframe, bg="White", bd=0)
        head = Label(loginforget,text="UPDATE LOGIN",font="Arial 20 bold")
        email = Label(loginforget, text="LOGIN ID:", font="Arial 12 bold")
        emal = Entry(loginforget, width=30, relief="groove", font="Arial 12 ", bd=2)
        send = Button(loginforget, image=sen,bd=0, command=lambda:[send_message(emal.get(),self)])
        send.image=sen
        back = Button(loginforget, image=log,bd=0, command=lambda: [loginforget.destroy(), self.login(t,9)])
        back.image=log
        # an Empty label to create space or to skip a line using pack

        space = Label(loginforget, text="")

        head.grid(row=0, column=1, columnspan=3, pady=4)
        space.grid(row=1)
        email.grid(row=2, column=2, sticky="w", pady=2, padx=2)
        emal.grid(row=3, column=2, sticky="ew", pady=2, padx=2)
        space.grid(row=4)
        send.grid(row=5, column=2, pady=2, padx=2)
        space.grid(row=6)
        back.grid(row=7, column=2,sticky='w', pady=3, padx=2)
        loginforget.pack()

    def sign_up(self):

        # resizing image use in button
        # --------------------------------------------------------------------#
        sign = Image.open("signup.jpg")
        sign = sign.resize((190, 40), Image.ANTIALIAS)
        sign = ImageTk.PhotoImage(sign)
        log = Image.open("Back_but.jpg")
        log = log.resize((140, 35), Image.ANTIALIAS)
        log = ImageTk.PhotoImage(log)
        # --------------------------------------------------------------------#

        #-----------------------------------------------  #
        login_signup = Frame(self.bframe, bg="White", bd=0)
        head = Label(login_signup, text="Sign up", font="Arial 20 bold")
        email = Label(login_signup, text="LOGIN ID:", font="Arial 12 bold")
        emal = Entry(login_signup, width=30, relief="groove", font="Arial 12 ", bd=2)
        username = Label(login_signup, text="USER NAME:", font="Arial 12 bold")
        name = Entry(login_signup, width=30, relief="groove", font="Arial 12 ", bd=2)
        paswd = Label(login_signup, text="PASSWORD:", font="Arial 12 bold", bd=2)
        password = Entry(login_signup, width=30, font="Arial 12 bold", relief="groove", bd=2, show="*")
        signup_btn = Button(login_signup, image=sign, bd=0,
                            command=lambda: [set_signup(emal.get(),name.get(),password.get())])
        signup_btn.image = sign
        back = Button(login_signup, image=log, bd=0, command=lambda: [login_signup.destroy(), self.login(t, 9)])
        back.image = log
        self.i = 0
        self.showpass = Button(login_signup, text="Show password", bd=0, fg='Blue',command=lambda :self.showpassword(password))
        # an Empty label to create space or to skip a line using pack

        space = Label(login_signup, text="")
        head.grid(row=0, column=1, columnspan=3, pady=4)
        space.grid(row=1)
        email.grid(row=2, column=2, sticky="w", pady=2, padx=2)
        emal.grid(row=3, column=2, sticky="ew", pady=2, padx=2)
        username.grid(row=4,column=2,sticky="w",pady=2,padx=2)
        name.grid(row=5,column=2,sticky="ew",pady=3,padx=2)
        paswd.grid(row=6,column=2,sticky="w",pady=2,padx=2)
        password.grid(row=7,column=2,sticky="ew",pady=3,padx=2)
        self.showpass.grid(row=8,column=2,sticky="e",pady=3,padx=2)
        signup_btn.grid(row=9, column=2, pady=2, padx=2)
        space.grid(row=10)
        back.grid(row=11, column=2, sticky='w', pady=3, padx=2)
        login_signup.pack()

    def showpassword(self,entry):
        if(self.i % 2 == 0):
            entry.config(show="")
            self.showpass.config(text="Hide password",fg='red')
            self.i+=1
        else:
            entry.config(show="*")
            self.showpass.config(text="Show password",fg='blue')
            self.i+=1



#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

                                                # OPTION BAR = SEARCHBAR

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

#optionbar have both search and right side frame
class optionbar():
    def __init__(self,t):
        #using canvas global variable
        global canvas
        # destroying old canvas
        canvas.pack_forget()

        #making new background
        #-----------------------------------------------------#

        #resizing iamge use in background
        second = Image.open("high.jpg")
        second = second.resize((990,550),Image.ANTIALIAS)
        second= ImageEnhance.Sharpness(second)
        second = second.enhance(7.0)
        second = ImageTk.PhotoImage(second)

        #making background
        canvas = Canvas(parent, width=992, height=700,scrollregion=(0,0,1000,1000),bg="#131d20")
        canvas.image = second
        canvas.create_image(0, 0, image=second, anchor="nw")

        #making scrollbar
        self.scroll = Scrollbar(parent, command=canvas.yview)

        #adding it to canvas
        canvas.config(yscrollcommand=self.scroll.set)
        self.scroll.pack(fill="y",side=RIGHT)
        canvas.pack(fill=BOTH, expand=True)

        #-----------------------------------------------------#

        # making a search bar
        self.search = Frame(canvas,bd=0)
        self.upframwe = Frame(self.search,bg="#dabf00")
        self.downframe = Frame(self.search,bg="#dabf00")

        # search.config(bg="#e4d2fc", bd=5)
        self.search.config(bg="#dabf00", bd=3)
        imag= Image.open("smart.png")
        imag = imag.resize((70,50),Image.ANTIALIAS)
        imag =ImageTk.PhotoImage(imag)
        icon = Label(self.search,image=imag)
        icon.image=imag
        icon.grid(row=0,column=0,rowspan=2)

        #makind Serachbox
        self.ent = Entry(self.downframe, width=70,state=NORMAL,relief=GROOVE,bd=3 ,font=("times new roman ",12,"bold"))

        #making search button
        self.b = Button(self.downframe, text="search",relief="groove", command=lambda: [lis_of_link.clear(),call(str(self.ent.get()))],bd=3
                        ,activebackground="yellow",font=("Arial",10,"bold"))

        # binding Enter key with search  button
        t.bind('<Return>', lambda event=None:[self.b.invoke()])

        #---------------------------------------------------------------------------------#
        #making forward and back button
        self.back = Button(self.downframe, text=" < ",relief="groove"
                            ,command=lambda: [for_back("back",str(self.ent.get()),self)],bd=3
                           ,activebackground="yellow",font=("Arial",10,"bold"))

        #binding ctrl+b key with back button
        t.bind("<Control-Key-b>", lambda event=None: [for_back("back",str(self.ent.get().replace("b","")),self)])

        #making forward button
        self.frwd = Button(self.downframe, text=" > ",relief="groove"
                            ,command=lambda: [for_back("forward",str(self.ent.get()),self)],bd=3,activebackground="yellow",font=("Arial",10,"bold"))

        #binding ctrl+f key with forward button
        t.bind("<Control-Key-f>", lambda event=None: [for_back("forward",str(self.ent.get()).replace("f",""),self)])

        #making home button
        try:
            self.home = Button(self.downframe, text="Home",relief="groove", command=lambda: [dt.btm.destroy(),self.putinSearch(""),freeup()],bd=3
                        ,activebackground="yellow",font=("Arial",10,"bold"))

            #binding home key with home button
            t.bind("<Home>",lambda event=None: [dt.btm.destroy(),self.putinSearch(""),freeup()])
        except:
            print(" ")

        #making a voice search button
        mic=Image.open("mic.png")
        mic= mic.resize((20,20),Image.ANTIALIAS)
        mic=ImageTk.PhotoImage(mic)
        self.speech = Button(self.downframe,image=mic,bg="white",bd=0
                             ,command=lambda:[lis_of_link.clear(), self.putinSearch("Listening....."),self.micsearch()])
        self.speech.image=mic
        # ----------------------------------------------------------------------------------#

        self.back.pack(side=LEFT,fill="y",padx=4)
        self.frwd.pack(side=LEFT,fill="y",padx=4)
        self.home.pack(side=LEFT, fill="y", padx=4)
        self.home.config(width=7)
        self.ent.pack(side=LEFT, padx=3)
        self.speech.pack(side=LEFT, padx=2)
        self.b.pack(side=LEFT,padx=3)

        # upframe
        self.wish=Button(self.upframwe,text="wishlist",activebackground="yellow",font=("Arial",10,"bold")
                       , bg='#dabf00',relief=GROOVE,bd=2,command=lambda :[wish(self)])
        self.rev_u = Button(self.upframwe, text="Reviews", activebackground="yellow", font=("Arial", 10, "bold")
                           , bg='#dabf00', relief=GROOVE, bd=2, command=lambda: [print("rev_u")])
        self.logout = Button(self.upframwe, text="log out", activebackground="yellow", font=("Arial", 10, "bold")
                           , bg='#dabf00', relief=GROOVE, bd=2,
                             command= lambda:[logout(self)])
        profile = Image.open("profile.png")
        profile = profile.resize((20, 20), Image.ANTIALIAS)
        profile = ImageTk.PhotoImage(profile)
        self.prof = Label(self.upframwe,image=profile,bg='#dabf00')
        self.prof.image=profile
        self.logid = Label(self.upframwe,text = log_id, font='Arial 12 bold',bg='#dabf00')


        self.prof.pack(side=LEFT,padx=2)
        self.logid.pack(side=LEFT,padx=4)
        #space.pack(side=RIGHT)
        self.logout.pack(side=RIGHT,padx=3)
        #self.rev_u.pack(side=RIGHT,padx=3)
        self.wish.pack(side=RIGHT,padx=3)

        self.upframwe.grid(row=1,column=2,sticky="nswe",pady=1)
        self.downframe.grid(row=0,column=2,sticky="nw",padx=5)

        #adding searchbar to canvas
        self.search_frame = canvas.create_window(3,3, anchor="nw", window=self.search)
        #self.search.pack(side=TOP,fill='x')



        #making right side menu bar   currently not used

        # rside = Frame(canvas,relief=GROOVE)
        # rside.config(bg="#7e7ec4",bd=3)
        # b1 = Button(rside, relief="groove",text="Appliance", width=20, command=lambda: [lis_of_link.clear(),self.putinSearch("Appliances"), call("Appliances")])
        # b2 = Button(rside, relief="groove", text="Mobile", command=lambda: [lis_of_link.clear(),self.putinSearch("Mobile"), call("Mobile")])
        # b3 = Button(rside, relief="groove", text="Head phones", command=lambda: [lis_of_link.clear(),self.putinSearch("Head Phones"), call("Head phones")])
        # b3.pack(fill="x", padx=2, pady=3)
        # b2.pack(fill="x", padx=2, pady=3)
        # b1.pack(fill="x", padx=2, pady=3)

#putinsearch method put the text of button in right side panel in search bar
    def putinSearch(self,txt):
        st = StringVar(t, value=txt)
        self.ent.config(textvariable=st)

#find the voice search
    def micsearch(self):
        pro = voice()
        self.putinSearch(pro)
        call(pro)

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

                               #product class=make frame of all product present on website

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

# product class makes the frame of searches on window
class product():
    def __init__(self,master,lis):
        self.name_lis = []
        self.btm = Frame(canvas,width=550)
        fnt=["Arial 10 bold", "Arial 13 bold", "Arial 10 "]
        self.lis=lis

        #==========================================================================================#

        try:

            #se=["#bab2de","#a0d0c4","#aca25a","#baacbc","#dad3d9","#a0d0c4"]

            # if not in the lis then it will raise type error
            if "NOT" in self.lis:
                # after error clear lia
                raise TypeError()
            #-------------------------------------------------#
            #for making object of % frames
            l = []
            for i in range(0, 7):
                self.la = Frame(self.btm, bg="#131d20")
                l.append(self.la)
                lis_of_link.append(self.lis[i]["link"])
                i += 1
            #--------------------------------------------------#

            #calling img function to show image of all product
            img = self.image()

            #==================================================================================#
            for p in range(0, 7):
                self.lab = imagebutton(l[p],p)
                self.lab.image = img[p]  # this is anchor image object to label
                self.lab.config(image=img[p])
                self.lanam = Label(l[p],text=self.lis[p].get("name"),fg="white",wraplength=600, bg='#131d20',font=fnt[0])
                self.laprice = Label(l[p],text=self.lis[p].get("price"),fg="white", bg='#131d20',font=fnt[1])
                self.laadd = Label(l[p], text=self.lis[p].get("address"),fg="white", bg='#131d20',font=fnt[2])
                self.btframe = Frame(self.btm,bg='#131d20')
                self.wish =  self.wsbutton(p)
                self.review = reviewbtn(p,self.btframe,lis[p])
                self.visit = mkButton(p,self.btframe)
                self.lab.grid(row=0, column=0, sticky="ns", rowspan=2)
                self.lanam.grid(row=0, column=1)
                self.laprice.grid(row=1, column=1)
                self.laadd.grid(row=1, column=2)
                self.wish.pack(side=RIGHT,fill="x",padx=5,pady=3)
                self.visit.pack(side=RIGHT,fill="x",padx=5,pady=3)
                self.review.pack(side=RIGHT, fill="x", padx=5, pady=3)
                l[p].pack(side=TOP, fill="x", pady=1)
                self.btframe.pack(fill="x")
                p += 1

            #create a window
            self.can_frame = canvas.create_window(10,70, anchor="nw", window=self.btm,tags="self.btm")

            #to expand btm frame on canvas
            self.FrameWidth()

            #to set the size of canvas wrt btm frame
            self.btm.bind("<Configure>", self.OnFrameConfigure)

            # to bind mouse wheel on ui for scroll from any where
            t.bind("<MouseWheel>",self._on_mousewheel)

        except BaseException as e:
            if "NOT" not in self.lis:
                self.lis = "ERROR"
                #to print the error message on console
                print(e)
                print(traceback.format_exc())
            self.la = Label(self.btm,text=self.lis,font="Arial 22 bold")
            self.la['background']='#856ff8'
            self.la.pack(fill="x")
            self.can_frame = canvas.create_window(10, 70, anchor="nw", window=self.btm)
            self.FrameWidth()

        #===============================================================================================#

#destroy the search frame
    def detr(self):
        self.btm.destroy()

#making object of image
    def image(self,n=7):
        img=[]
        for i in range(0,n):
            im = Image.open(str(i)+".jpg")
            im = im.resize((70,65), Image.ANTIALIAS)
            im = ImageTk.PhotoImage(im)
            img.append(im)
            i+=1
        return img

#function to stick frame on all side of canvas
    def FrameWidth(self,l=0):
        canvas.itemconfig(self.can_frame, width=canvas.winfo_width()-10-l)

#function to change size of canvas wrt to btm frame
    def OnFrameConfigure(self, event):
        canvas.configure(scrollregion=canvas.bbox("all"))

#function to add event listener of mouse wheel on canvas to scroll canvas
    def _on_mousewheel(self, event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

#function to make interface for adding product in wish list
    def wsbutton(self,n):
        return Button(self.btframe, text="+ Wishlist", font=("times new roman ", 8, "bold"), activebackground = "yellow", command = lambda:self.Add(n))

#add images to wish list directory
    def Add(self,n):
        try:
            self.name_lis = con.prod_lis(log_id)
            if self.lis[n].get("name") not in self.name_lis :
                con.addwish(log_id,self.lis[n])
                #print(lis_of_wish)
                src = str(n)+".jpg"
                des = "wishlist"
                sh.copy(src,des)
                src = os.path.join("wishlist", str(n)+".jpg")
                des = os.path.join("wishlist", str(self.lis[n].get("name"))+".jpg")
                os.renames(src, des)
        except:
            print(" ")


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

                            #class wishlist = to display list of wishlist

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

class wishlist():

    def __init__(self):
        fnt = ["Arial 10 bold", "Arial 13 bold", "Arial 10 "]
        global canvas
        canvas.pack_forget()
        # ==========================================================================================#

        third = Image.open("wishlist.jpg")
        third = third.resize((990, 550), Image.ANTIALIAS)
        third = ImageTk.PhotoImage(third)
        canvas = Canvas(parent, width=992, height=700, scrollregion=(0, 0, 1000, 1000), bg="#131d20")
        canvas.image = third
        canvas.create_image(0, 0, image=third, anchor="nw")
        back = Image.open("Back_but.jpg")
        back = back.resize((145, 50), Image.ANTIALIAS)
        back = ImageTk.PhotoImage(back)
        bak = Button(canvas, image=back,command=lambda :[self.wish.destroy(),optionbar(t),scroll.pack_forget()])
        bak.image = back
        #bak.pack(side=LEFT)
        canvas.create_window(0, 0, anchor="nw", window=bak)
        # making scrollbar
        scroll = Scrollbar(parent, command=canvas.yview)
        # adding it to canvas
        canvas.config(yscrollcommand=scroll.set)
        scroll.pack(fill="y",side=RIGHT)
        self.wish = Frame(canvas)
        canvas.pack(fill=BOTH, expand=True)

        try:

            # se=["#bab2de","#a0d0c4","#aca25a","#baacbc","#dad3d9","#a0d0c4"]

            # -------------------------------------------------#
            # for making object of % frames
            l = []
            lis = con.fetchpod(log_id)
            lis_of_link.clear()
            self.pr_name = con.prod_lis(log_id)
            for i in range(0, len(self.pr_name)):
                self.wla = Frame(self.wish, bg="#131d20")
                l.append(self.wla)
                lis_of_link.append(lis[i]["link"])
                i += 1
            # --------------------------------------------------#

            # calling img function to show image of all product
            img = self.mkimage(n=len(self.pr_name))

            # ==================================================================================#
            for p in range(0, len(self.pr_name)):
                self.wlab = imagebutton(l[p], p)
                self.wlab.image = img[p]  # this is anchor image object to label
                self.wlab.config(image=img[p])
                self.wlanam = Label(l[p], text=lis[p].get("name"), fg="white", wraplength=600, bg='#131d20',
                                    font=fnt[0])
                self.wlaprice = Label(l[p], text=lis[p].get("price"), fg="white", bg='#131d20', font=fnt[1])
                self.wlaadd = Label(l[p], text=lis[p].get("address"), fg="white", bg='#131d20', font=fnt[2])
                self.wbtframe = Frame(self.wish, bg='#131d20')
                self.wvisit = mkButton(p, self.wbtframe)
                self.Reminder = rembutton(p=p,frame=self.wbtframe,lis=lis)
                self.wlab.grid(row=0, column=0, sticky="ns", rowspan=2)
                self.wlanam.grid(row=0, column=1)
                self.wlaprice.grid(row=1, column=1)
                self.wlaadd.grid(row=1, column=2)
                self.Reminder.pack(side=RIGHT, fill="x", padx=5, pady=3)
                self.wvisit.pack(side=RIGHT, fill="x", padx=5, pady=3)
                l[p].pack(side=TOP, fill="x", pady=1)
                self.wbtframe.pack(fill="x")
                p += 1

            # create a window
            self.par_can = canvas.create_window(0, 53, anchor="nw", window=self.wish, tags="self.wish")

            # to set the size of canvas wrt btm frame
            self.wish.bind("<Configure>", lambda event:canvas.configure(scrollregion=canvas.bbox("all")))

            #to adjust size of window on canvas
            global t
            t.bind("<Configure>",lambda event:canvas.itemconfig(self.par_can,width=canvas.winfo_width() - 10))

            # to make action listerner of mousewheel
            t.bind("<MouseWheel>", lambda event:canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

        except BaseException as e:

            if "NOT" not in lis:
                lis = "ERROR"
                print(e)
                print(traceback.format_exc())
            self.la = Label(self.wish, text=lis, font="Arial 22 bold")
            self.la['background'] = '#856ff8'
            self.la.pack(fill="x")
            self.can_frame = canvas.create_window(10, 70, anchor="nw", window=self.wish)
            # to make erroe maessafe same width as canvas
            #t.bind("<Configure>",lambda event:canvas.itemconfig(self.par_can,width=canvas.winfo_width() - 10))

    # making object of image
    def mkimage(self, n):
        img = []
        for i in range(0,n):
            add = os.path.join("wishlist", str(self.pr_name[i]+".jpg"))
            im = Image.open(add)
            im = im.resize((70, 65), Image.ANTIALIAS)
            im = ImageTk.PhotoImage(im)
            img.append(im)
            i += 1
        return img

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

t = Tk()
t.iconbitmap(r"icon.ico")

parent = Frame(t)

# The (450, 350) is (height, width)
#resizing image by using PIL
image = Image.open('new.jpg')
image = image.resize((990,550), Image.ANTIALIAS)
bg = ImageTk.PhotoImage(image)

# making canvas and adding image in back ground
canvas = Canvas(parent, width=990, height=600,bg="black")

parent.pack(fill=BOTH)
def first():
    canvas.image=bg
    #-->ANCHOR TAG FOR IMAGE
    canvas.create_image(0, 0, image=bg, anchor="nw")

    #creating text on background image
    canvas.create_text(300, 40, text="We help you to save money",fill="White",font="Times 20 bold")
    canvas.create_text(800, 75, text="SKARS", fill="black", font="Arial 25 bold")
    canvas.pack(fill=BOTH, expand=True)
    #calling making obj of header

    h = header(t)


first()

t.mainloop()


