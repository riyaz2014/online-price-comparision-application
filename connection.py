import mysql.connector as mysql
from datetime import datetime
import send_email as send
import  webbrowser as wb
#making connection
mydb = mysql.connect(host="localhost",user="root",passwd="",database="skars shopping")
#mydb = mysql.connect(host="localhost",user="root",passwd="",database="fir")
mycur = mydb.cursor()
#taking current time and date
a = datetime.now()


def signup(username,log_id,passwd):
    try:
        sq ='insert into login (log_id,pass_word,User_name) values (%s,%s,%s)'
        val = (log_id,passwd,username)
        mycur.execute(sq,val)
        mydb.commit()
    except:
        print("Error")



def login(log_id,passwd='0'):
    try:
        sq = "select pass_word from login where log_id= %s"
        val = (log_id,)
        mycur.execute(sq,val)
        result = mycur.fetchone()
        if passwd in result:
            return True
        else:
            return False
    except:
        print("login Error")


#login('kayub4947@gmail.com',)
def addwish(log_id,dic):
    try:
        sq = 'insert into wishlist (log_id,Product_name,price,Store_name,link) values (%s,%s,%s,%s,%s)'
        val = (log_id,dic.get("name"),dic.get("price"),dic.get("address"),dic.get("link"))
        mycur.execute(sq,val)
        mydb.commit()
    except:
        print("Error")


def addrem(p_name,log_id,time):
    try:
        sq1="select Wish_id from wishlist where log_id=%s and Product_name=%s"
        val1 = (log_id,p_name)
        mycur.execute(sq1,val1)
        res = mycur.fetchone()
        wish_id = res[0]
        date = a.strftime('%Y-%m-%d')
        rem_tm = a.strftime( '%H:%M')
        sq2 = 'insert into reminder_list (Wish_id,rem_time,rem_date,check_tm) values (%s,%s,%s,%s)'
        val2 = (wish_id,rem_tm,date,time)
        mycur.execute(sq2,val2)
        mydb.commit()
    except:
        print("Error")


def addrev_u(log_id,rev_u,p_name,star):
    try:
        sq = 'insert into reviews (log_id,Product_name,review,star,date) values (%s,%s,%s,%s,%s)'
        date = a.strftime('%Y-%m-%d')
        val = (log_id,p_name,rev_u,star,date)
        mycur.execute(sq,val)
        mydb.commit()
    except:
        print("Error")

def fetch_rev_u(pr_name):
    try:
        sq = "select log_id,review,star,date from reviews where Product_name=%s"
        val = (pr_name,)
        mycur.execute(sq,val)
        #for i in mycur.fetchall():
        res = mycur.fetchall()
        lis_of_rev=[]
        for elem in res:
            dic ={"review":elem[1],'star':elem[2],'date':elem[3]}
            lis_of_rev.append(dic)
        j=0
        for i in res:
            sq1='select User_name from login where log_id=%s'
            val1 = (i[0],)
            mycur.execute(sq1, val1)
            name = mycur.fetchone()[0]
            lis_of_rev[j]['name']=name
            j+=1
        return lis_of_rev

    except:
        print('error')


def fetchpod(log_id):
    try:
        sq = 'select Product_name,price,Store_name,link from wishlist where log_id = %s '
        val = (log_id,)
        mycur.execute(sq,val)
        li = []
        for i in mycur.fetchall():
            di = {'name': i[0], 'price': i[1], 'address':i[2],'link':i[3]}
            li.append(di)

        return li
    except:
        print("Error")


def prod_lis(log_id):
    try:
        sq = 'select Product_name from wishlist where log_id = %s '
        val = (log_id,)
        mycur.execute(sq,val)
        li = []
        for i in mycur.fetchall():
            li.append(i[0])
            #print(i)
        #wb.open_new(i[3])
        #print(li)
        return li
    except:
        print("Error")

def fetchpass(log_id):
    try:

        sq = 'select pass_word from login WHERE log_id =%s'
        val =(log_id,)
        mycur.execute(sq,val)
        passwd = mycur.fetchone()
        if passwd==None:
            return 1
        s = send.send_email()
        s.send_pass(passwd=passwd,id=log_id)
        return 0
    except:
        print("error")

def check_rev_u(log_id,pr_name):
    try:
        sq = 'select log_id from reviews where Product_name=%s'
        val=(pr_name,)
        mycur.execute(sq, val)
        cust = mycur.fetchall()
        for i in cust:
            if i[0] == log_id:
                return False
        return True
    except:
        print("error")

#print(check_rev_u('kayub4947@gmail.com','Redmi Note 10 Shadow Black 6GB+128GB'))


#fetch_rev_u('Redmi Note 10 Shadow Black 6GB+128GB')

#dic = {'name':"mi note 5",'price':'10000','address':"mi.com", "link":'www.google.com'}
#mycur.execute('select * from role')
#print(li)
#fetchpod('kayub4947@gmail.com')
#addwish('kayub4947@gmail.com',dic)
#addrem('mi note 5','kayub4947@gmail.com',5)
#rev = "This is very mast product you should buy it quickly "
#addrev_u('kayub4947@gmail.com',rev,'mi note 5',4)
#print(mycur.rowcount, "record inserted.")
#prod_lis('kayub4947@gmail.com')

