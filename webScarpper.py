import requests as rq
import bs4 as bs
import webbrowser as wb
import time as tm
import os

l =[]

class webScrapper():
    def get(self,name):
        li = name.split(" ")
        name = li[0]
        snapname=li[0]
        for i in range(1,len(li)):
            name = name+"+"+li[i]
            snapname=snapname+"%20"+li[i]

        link = {"flipkart":"https://www.flipkart.com/search?q=" + name + "&sid=tyy%2C4io&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_2_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_2_na_na_na&as-pos=1&as-type=RECENT&suggestionId=" + name + "%7CMobiles&requestId=5e68ee47-f162-4f05-a81b-6a378267415e&as-backfill=on"
                 ,"Amazon" :"https://www.amazon.in/s?k="+name+"&ref=nb_sb_noss_2"
                 , "Snapdeal":"https://www.snapdeal.com/search?keyword="+snapname+"&santizedKeyword=&catId=&categoryId=0&suggested=false&vertical=&noOfResults=20&searchState=&clickSrc=go_header&lastKeyword=&prodCatId=&changeBackToAll=false&foundInAll=false&categoryIdSearched=&cityPageUrl=&categoryUrl=&url=&utmContent=&dealDetail=&sort=rlvncy"
                 , "Google" : "https://www.google.com/search?tbm=shop&sxsrf=ALeKk010apoTNUr-xh7l4_hRMJ_hoH88UA%3A1613551493264&source=hp&ei=hdcsYOW_DZmR9QO-xY-oAQ&q="+name+"&oq=&gs_lcp=Cgtwcm9kdWN0cy1jYxABGAAyBwgjEOoCECcyCAgAEOoCEI8BMggIABDqAhCPATIICAAQ6gIQjwEyCAgAEOoCEI8BMggIABDqAhCPATIICAAQ6gIQjwEyCAgAEOoCEI8BMggIABDqAhCPATIICAAQ6gIQjwEyCAgAEOoCEI8BUABYAGC0K2gBcAB4AIABAIgBAJIBAJgBAKoBD3Byb2R1Y3RzLWNjLXdperABCw&sclient=products-cc"

                }
        return link


    def scrapgog(self, link):
        product = rq.get(link)
        soup = bs.BeautifulSoup(product.text, features="html.parser")
        for j in range(0, 9):
            dlet = soup.find("div", {"class": 'dD8iuc d1BlKc'})
            dlet = str(dlet)
            soup = str(soup)
            soup = soup.replace(dlet, "8")
            soup = bs.BeautifulSoup(soup, features="html.parser")
            j += 1

        liofProd = []

        info = soup.find_all("div", class_='P8xhZc')
        img = soup.find_all("div", class_="oR27Gd")
        for i in range(0, 7):

            infor = info[i].find("div", class_='rgHvZc').get_text()
            add = info[i].find("div", class_='dD8iuc').get_text()
            price = info[i].find("span", class_="HRLxBb").get_text()
            anchor = info[i].find("a").get("href")
            im = img[i].find("img").get("src")
            l.append(im)
            if "/url?q=" in anchor:
                anchor = anchor.replace("/url?q=", "")
            # print(str(i)+" "+infor)
            # print(str(i)+" "+price)
            add = add.replace(price, "")
            # print(str(i) + " " + add)
            # print(str(i) + " " + price)
            # print(str(i) + " " + anchor)
            dic = {"name": str(infor), "price": str(price), "address": str(add), "link": str(anchor)}
            liofProd.append(dic)
            i += 1

        return liofProd

    def download(self):
        for i in range(0,7):
            with open(str(i)+".jpg","wb") as f:
                im = rq.get(l[i])
                f.write(im.content)

    def delete(self):
        l.clear()
        for i in range(0,7):
            os.remove(str(i)+".jpg")

