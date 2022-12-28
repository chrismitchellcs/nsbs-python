from flask import Blueprint, render_template, request
from urllib.error import *
import requests
from bs4 import BeautifulSoup
import smtplib


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")

@views.route('/contact.html', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name =  request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]
        # send_email(name, email, subject, message)
    
        
    return render_template("contact.html")

@views.route('/service.html', methods=['GET', 'POST'])
def service():
    return render_template("service.html")

@views.route('/shop.html', methods=['GET', 'POST'])
def shop():
    return render_template("shop.html")

@views.route('/bikes.html', methods=['GET', 'POST'])
def bikes():
    return render_template("bikes.html")

@views.route('/bikesPB.html', methods=['GET', 'POST'])
def bikesPB():
    result_list = getBikes()
    return render_template("bikesPB.html", result = result_list)

def send_email(name, email, subject, message):
    email_message = f"Subject:{subject}\n\nName: {name}\nEmail: {email}\nSubject: {subject}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login('chrismitch774@gmail.com', 'xinxvonhqmkhdmrk')
        connection.sendmail('chrismitch774@gmail.com', 'chrismitch774@gmail.com', email_message)



class Result:
    src = ""
    desc = ""
    mat = ""
    wheelsize = ""
    size = ""
    front_travel = ""
    rear_travel = ""
    price = ""
    bike_page = ""

    def __init__(self, src, desc, mat, wheelsize, size, front_travel, rear_travel, price, bike_page):
        self.src = src
        self.desc = desc
        self.mat = mat
        self.wheelsize = wheelsize
        self.size = size
        self.front_travel = front_travel
        self.rear_travel = rear_travel
        self.price = price
        self.bike_page = bike_page
    

    def make_result(src, desc, mat, wheelsize, size, front_travel, rear_travel, price, bike_page):
        result = Result(src, desc, mat, wheelsize, size, front_travel, rear_travel, price, bike_page)
        return result

def getBikes(): 
    result_list = []
    page = requests.get("https://www.pinkbike.com/u/north-shore-bike-shop/buysell/")
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all('table')
    for i, result in enumerate(results):
        if (i % 2) == 0:
            
            detail = result.find_all('div', {"class": "itemdetail"})
            if len(detail) == 5:
                # print(result)
                frame_size = detail[0].getText()
                wheel_size = detail[1].getText()
                material = detail[2].getText()
                front_travel = detail[3].getText()
                rear_travel = detail[4].getText()

                price = result.find_all('td', {"class": "bsitem-price"})
                price = price[0].getText()

                website = result.find_all('a')
                href = website[1].get('href')
                desc = website[1].getText()

                newPage = requests.get(href)
                newSoup = BeautifulSoup(newPage.content, "html.parser")
                images = newSoup.find_all('div', {"id": "buysell-image"})
                if len(images) == 1:
                    src = images[0]['data-fullimageurl']
                    result = Result(src, desc, material, wheel_size, frame_size, front_travel, rear_travel, price, href)
                    result_list.append(result)
        
        # print(result)
        # if (i % 2) == 0:
        #     item = result.find_all('b')
        #     if len(item) == 8:
        #         price = item[7].getText()
        #         print(price)
        #     if len(item) == 6:
        #         price = item[5].getText()
        #     item = result.find_all('a')
        #     # get hd image from actual page
        #     bike_page = item[0]['href']
        #     newPage = requests.get(bike_page)
        #     newSoup = BeautifulSoup(newPage.content, "html.parser")
        #     images = newSoup.find_all('div', {"id": "buysell-image"})
        #     if len(images) == 1:
        #         src = images[0]['data-fullimageurl']
        #     item = result.find_all('a')
        #     desc = item[1].getText()
        #     item = result.find_all('div')
        #     # handle FS 
        #     if (len(item) == 7):
        #         mat = item[4]
        #         mat = mat.getText()
        #         wheelsize = item[3]
        #         wheelsize = wheelsize.getText()
        #         size = item[2]
        #         size = size.getText()
        #         front_travel = item[5]
        #         front_travel = front_travel.getText()
        #         rear_travel = item[6]
        #         rear_travel = rear_travel.getText()
        #         result = Result(src, desc, mat, wheelsize, size, front_travel, rear_travel, price, bike_page)
        #         result_list.append(result)
        #     if (len(item) == 4):
        #         pass
        #     if (len(item) == 5):
        #         pass

    return result_list
            
        

            
            
    
