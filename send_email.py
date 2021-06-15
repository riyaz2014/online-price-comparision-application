import smtplib as sm
import random as r

class send_email():
    def send_rem(self,pro,add,id):
        emoji = u"\U0001F38A"
        self.message = "     Good news! \n     [{}] \n\n     Added to your wishlist had recent decrease in its price on {}".format(pro,add)
        #print(self.message)
        sub = "Price reduction announcement"
        self.message = "Subject: {} \n\n{}".format(sub,self.message)
        try:
           server = sm.SMTP("smtp.gmail.com", 587)
           server.starttls()
           server.login("skars.shopping10@gmail.com", "skars@1234")
           server.sendmail("skars.shopping10@gmail.com",id, self.message)

        except Exception as e:
            print(e)

    def send_pass(self,passwd,id):
        emoji = u"\U0001F38A"
        self.message = "Your password of SKARS shopping center is [{}]".format(passwd)
        # print(self.message)
        sub = "Password sender"
        self.message = "Subject: {} \n\n{}".format(sub, self.message)
        try:

            server = sm.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login("skars.shopping10@gmail.com", "skars@1234")
            server.sendmail("skars.shopping10@gmail.com", id, self.message)

        except Exception as e:
            print(e)


#e=send_email()
#e.send_pass("123456789","riyaztech2000@gmail.com")
#e.send_pass('12345678',"kayub4947@gmail.com")
#email("Product","Project","2019mohdayub.choudhari@ves.ac.in")