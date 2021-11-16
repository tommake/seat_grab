# coding:utf-8
import requests
import re
import time
import json
import getopt
import sys
from datetime import date
from datetime import timedelta
import datetime
from bs4 import BeautifulSoup


url_login = 'http://authserver.qdu.edu.cn/authserver/login?service=http://csyy.qdu.edu.cn:8080/loginmall.aspx'

login_post = 'http://authserver.qdu.edu.cn/authserver/login?service=http://csyy.qdu.edu.cn:8080/loginmall.aspx'


def login():
    z.headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    s = z.get(url_login)
    html = s.text
    pattern_lt = r'name="lt" value="(.*?)"'
    lt = re.findall(pattern_lt, html)
    print(lt)
    login_data = {
        'username': '2019206728',
        'password': 'Aa123456',
        'lt':lt,
        'dllt':'userNamePasswordLogin',
        'execution':'e1s1',
        '_eventId':'submit',
        'rmShown':'1'
    }
    s1 = z.post(url=login_post, data=login_data)
    return z

def edit_y_params(public_day,time1,time2,time3,time4,dev_id):
    y_params = {
        'dialogid':'' ,
        'dev_id': dev_id,
        'lab_id': '',
        'kind_id': '',
        'room_id': '',
        'type': 'dev',
        'prop': '',
        'test_id': '',
        'term': '',
        'Vnumber': '',
        'classkind': '',
        'test_name': '',
        'start':public_day+time1,
        'end':public_day+time2 ,
        'start_time': time3,
        'end_time': time4,
        'up_file': '',
        'memo': '',
        'act': 'set_resv',
        '_': '',
    }
    return y_params

y_url = 'http://csyy.qdu.edu.cn:8080/ClientWeb/pro/ajax/reserve.aspx'

order_morning1=' 08:00'
order_morning2=' 14:00'
order_morning3='0800'
order_morning4='1400'

order_afternoon1=' 14:00'
order_afternoon2=' 20:00'
order_afternoon3='1400'
order_afternoon4='2000'

dev_id=['100456055','100456054','100456056','100456057','100456061']
#The seats are 079,078,080,081,085

id=0
month_31=[1,3,5,7,8,10,12]
month_30=[4,6,9,11]
month_28=[28]

while True:  
    z = requests.Session()  

    flag=0 
    sub_flag=1  
    success_flag=False   
    success_afternoon_flag=False 
    success_morning_flag=False
    id=0
    
    while True:
        my_hour=datetime.datetime.now().hour
        my_minute=datetime.datetime.now().minute
        if my_hour==0 and my_minute>=0:   
            flag+=1
            year=str(datetime.datetime.now().year)  
            month=str(datetime.datetime.now().month)
            day=datetime.datetime.now().day
            
            if month in month_31:   
                if datetime.datetime.now().day==31:
                    if month==12:
                        month=1
                        day=1
                    else:
                        month+=1
                        day=1
                else:
                    day+=1
            elif month in month_30:
                if datetime.datetime.now().day==30:
                    month+=1
                    day=1
                else:
                    day+=1
            else:
                if datetime.datetime.now().day==28:
                    month+=1
                    day=1
                else:
                    day+=1
            
            day=str(day)
            today_date=year+'-'+month+'-'+day   
            print("{}Th seat grab".format(flag))
            if not success_flag:
                z=login() 
                s2 = z.get(url_login)
                if s2.url=='http://csyy.qdu.edu.cn:8080/ClientWeb/xcus/ic2/Default.aspx':
                    success_flag=True
                    print("The website is successfully logged in and starts to grab seats!")
            else:
                print("The website is already logged in, try to grab a seat again!")
        
            time.sleep(3) 
            my_params1=edit_y_params(today_date,order_morning1,order_morning2,order_morning3,order_morning4,dev_id[id])
            my_params2=edit_y_params(today_date,order_afternoon1,order_afternoon2,order_afternoon3,order_afternoon4,dev_id[id])

            if not success_morning_flag:
                data_back1=z.get(url=y_url,data=my_params1)
                res=json.loads(data_back1.text) 
                print(res)
                back_message1=res['msg']  
                if back_message1 == '操作成功！':
                    success_morning_flag=True  
                    print("The morning seat has been reserved！")
                    time.sleep(5) 
                else:
                    print("The morning seat reservation failed, waiting for the next seat grab！")

            if not success_afternoon_flag:
                data_back2=z.get(url=y_url,data=my_params2)
                res=json.loads(data_back2.text) 
                print(res)
                back_message2=res['msg']  
                if back_message2 == '操作成功！':
                    success_afternoon_flag=True    
                    print("The afternoon seat has been reserved！")
                    time.sleep(5)  
                else:
                    print("Seat reservation in the afternoon failed, waiting for the next seat grab！")

            time.sleep(2)
            if flag>10:
                print("Too many times of occupying seats, in order to reduce the pressure on the server, the program has been terminated！")
                break
            if success_afternoon_flag and success_morning_flag:
                print("Grabbed all the seats and stopped grabbing seats！")
                break
            else:
                if flag%2==0:
                    id+=1
                    print("The {}th seat failed to grab the seat, and the seat has been switched to the next seat to start grabbing!".format(id))
        else:
            print("It's not time to grab a seat, please wait {}".format(sub_flag))
            cur=str(datetime.datetime.now())
            print("current time：{}".format(cur))
            sub_flag+=1
            if datetime.datetime.now().hour==23 and datetime.datetime.now().minute==59:
                distance_time=60-datetime.datetime.now().second
                time.sleep(distance_time+2)
            else:
                time.sleep(10)
       
    if success_afternoon_flag and success_morning_flag:
        print("All seats reserved successfully！")
        print("Number of seat grabs:{}".format(flag))
    else:
        if success_morning_flag:
            print("The morning seat reservation is successful！")
            print("Number of seat grabs:{}".format(flag))
        elif success_afternoon_flag:
            print("Seat reservation in the afternoon is successful！")
            print("Number of seat grabs:{}".format(flag))
        else:
            print("Failed to grab a seat and did not grab a suitable seat！")
            print("Number of seat grabs:{}".format(flag))
    
    y_params1 = {
        'sta':'1',
        'lab':'100455521',
        'dev':dev_id[id],
        'msn':''
    }  
    
    y_params2 ={
        'Userin':'true'
    }
    
    sub_url='http://csyy.qdu.edu.cn:8080/Pages/WxSeatSign.aspx'
    
    sign_morning_success=False
    sign_afternoon_success=False
    morning_post_flag=0     
    afternoon_post_flag=0  
    time_flag=1  
    success_flag=False

    z = requests.Session()  
    while True:
        my_hour=datetime.datetime.now().hour
        my_minute=datetime.datetime.now().minute
        if my_hour==8 and my_minute>=2:
            morning_post_flag+=1
            
            if morning_post_flag>10:
                print("Too many attempts in order to reduce the pressure on the server, this run has been terminated!")
                break
            
            if not success_flag:
                z=login() 
                s2 = z.get(url_login)
                if s2.url=='http://csyy.qdu.edu.cn:8080/ClientWeb/xcus/ic2/Default.aspx':
                    success_flag=True
                    print("The website is successfully logged in and starts to grab seats!")
            else:
                print("The website is already logged in, try to grab a seat again!")
            time.sleep(3) 
                
            if not sign_morning_success:   
                z.get(url=sub_url,data=y_params1)
                data_back3=z.get(url=sub_url,data=y_params2)
                
                bsobj=BeautifulSoup(data_back3.text)
                key1=bsobj.find("p")
                key2=str(key1.text)
                
                if key2=='操作成功':
                    sign_morning_success=True
                    print("Sign in successfully in the morning")
                    time.sleep(5) 
                    break
                else:
                    print("This check-in failed, wait for retry")
                    time.sleep(20)
        else:
            print("The morning time is not up, please wait!{}".format(time_flag))
            cur=str(datetime.datetime.now())
            print("current time:{}".format(cur))
            time_flag+=1
            time.sleep(10)

            
            
    z = requests.Session() 
    success_flag=False
    time_flag=1
    
    while True:
        my_hour=datetime.datetime.now().hour
        my_minute=datetime.datetime.now().minute
        if my_hour==14 and my_minute>2:
            afternoon_post_flag+=1
            
            if afternoon_post_flag>10:
                print("Too many attempts in order to reduce the pressure on the server, this run has been terminated!")
                break

            if not success_flag:
                z=login() 
                s2 = z.get(url_login)
                if s2.url=='http://csyy.qdu.edu.cn:8080/ClientWeb/xcus/ic2/Default.aspx':
                    success_flag=True
                    print("The website is successfully logged in and starts to grab seats!")
            else:
                print("The website is already logged in, try to grab a seat again!")
            time.sleep(3) 
                
            if not sign_afternoon_success:   
                z.get(url=sub_url,data=y_params1)
                data_back3=z.get(url=sub_url,data=y_params2)
                bsobj=BeautifulSoup(data_back3.text)
                key1=bsobj.find("p")
                key2=str(key1.text)
                
                if key2=='操作成功':
                    sign_afternoon_success=True
                    print("Sign in successfully in the afternoon")
                    time.sleep(5) 
                    break
                else:
                    print("This check-in failed, wait for retry")
                    time.sleep(20)
        else:
            print("It’s not time in the afternoon, please wait!{}".format(time_flag))
            cur=str(datetime.datetime.now())
            print("current time：{}".format(cur))
            time.sleep(10)
            time_flag+=1
            
print("The program exits abnormally, logic error!")
        
        