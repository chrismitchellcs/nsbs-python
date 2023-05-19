from flask import Blueprint, render_template, request, redirect, flash
from urllib.error import *
import requests
from bs4 import BeautifulSoup
import smtplib


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")

@views.route('/contact/<info>', methods=['GET', 'POST'])
def contact(info):
    # if request.method == 'POST':
    #     name =  request.form["name"]
    #     email = request.form["email"]
    #     subject = request.form["subject"]
    #     message = request.form["message"]
    #     send_email(name, email, subject, message)
    
    # if request.method == 'GET':
    if info == '0':
        return render_template("contact.html")
    else:
        return render_template("contactsent.html")

@views.route('/form', methods=['POST'])
def form():
    name =  request.form["name"]
    email = request.form["email"]
    subject = request.form["subject"]
    message = request.form["message"]
    send_email(name, email, subject, message)
    flash("you are successfuly logged in")  
    return redirect("/contact/1")

@views.route('/service', methods=['GET', 'POST'])
def service():
    return render_template("service.html")

@views.route('/shop', methods=['GET', 'POST'])
def shop():
    return render_template("shop.html")

@views.route('/bike', methods=['GET', 'POST'])
def bikes():
    result_list = getBikes()
    return render_template("bikes.html", result = result_list)

@views.route('/bikesPB', methods=['GET', 'POST'])
def bikesPB():
    result_list = getBikes()
    return render_template("bikesPB.html", result = result_list)

def send_email(name, email, subject, message):
    email_message = f"Subject:{subject}\n\nName: {name}\nEmail: {email}\nSubject: {subject}\nMessage:\n{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        # connection.starttls()
        # connection.login('chrismitch774@gmail.com', 'xinxvonhqmkhdmrk')
        # connection.sendmail('chrismitch774@gmail.com', 'chrismitch774@gmail.com', email_message)
        connection.starttls()
        connection.login('northshorebikeshop@gmail.com', 'ekicbgetmbnlwbam')
        connection.sendmail('northshorebikeshop@gmail.com', 'northshorebikeshop@gmail.com', email_message)



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
    results = soup.find_all("div", {"class": "bsitem"})
    for i, result in enumerate(results):
        # if (i == 0):
            # print(result)
            table = result.find_all("tr", {"class": "bsitem-table"})[0]
            src = table.find_all("a")[0].find_all("img")[0]["src"]
            
            # print(alink)
            item_details = result.find_all("div", {"class": "bsitem-title"})[0]
            bike_type = item_details.find_all("br")[0].next_sibling.strip()
            if (bike_type == "Enduro Bikes" or bike_type == "Trail Bikes" or bike_type == "Downhill Bikes" or bike_type == "Dirt Jump Bikes"):
                title = item_details.find_all("a")[0]
                website = title['href']
                desc = title.getText()
                more_details = item_details.find_all("div", {"class": "itemdetail"})
                frame_size = more_details[1].getText()
                wheel_size = more_details[2].getText()
                
                if (bike_type == "Dirt Jump Bikes"):
                    front_travel = ""
                    rear_travel = ""
                    material = ""
                else:
                    front_travel = more_details[4].getText()
                    rear_travel = more_details[5].getText()
                    material = more_details[3].getText()
                price = result.find_all('td', {"class": "bsitem-price"})[0].getText()
                # newPage = requests.get(website)
                # newSoup = BeautifulSoup(newPage.content, "html.parser")
                # images = newSoup.find_all('div', {"id": "buysell-image"})
                # if len(images) == 1:
                    # src = images[0]['data-fullimageurl']
                result = Result(src, desc, material, wheel_size, frame_size, front_travel, rear_travel, price, website)
                result_list.append(result)
        
        
        
        

    return result_list
            
        

            
            
    
