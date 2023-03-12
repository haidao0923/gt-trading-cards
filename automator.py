from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import pymongo
import gridfs
import json
import os
import hashlib

with open("config.json", 'r') as f:
    config = json.load(f)
print(config['mongoDBURI'])

chrome_options = Options()
#chrome_options.add_argument("--headless")

def morph_image(image1, image2):
    driver = webdriver.Chrome(options=chrome_options)
    url = 'https://en.pixiz.com/template/Fusion-of-two-faces-1630'
    driver.get(url)

    driver.find_element(By.ID, "upload-file-1").send_keys(image1)
    driver.find_element(By.ID, "upload-file-2").send_keys(image2)
    driver.find_element(By.ID, "upload-submit-button").click()
    link = driver.find_element(By.XPATH, '//*[@id="p-result"]/div/div[3]/div/div[3]/ul/li[5]/a').get_attribute('href')
    print("Test", link)
    morphed_image = requests.get(link).content
    with open("morphed_image.png", 'wb') as handler:
        handler.write(morphed_image)
    return morphed_image


image1 = os.path.abspath("jacob_abernethy_0.png")
image2 = os.path.abspath("joy_arulraj_0.png")
morphed_image = morph_image(image1, image2)

client = pymongo.MongoClient(config['mongoDBURI'])
db = client.gttc

def add_user(username, password):
    db.users.insert_one({
        "username": username,
        "password": password,
        "cards": []
    })

def get_user(username):
    user = db.users.find_one({"username": username})
    return user

def add_card_to_user(username, card_id):
    db.users.update_one({"username": username}, {'$push': {'cards': card_id}})

def add_card(name, image):
    fs = gridfs.GridFS(db)
    #print("Image Before", morphed_image)
    #image_bytes = image.read()
    id = hashlib.sha256(image).hexdigest()
    image_id = fs.put(image)
    #print("Len", len(id), len(image_id))
    #image = fs.get(id).read()
    #print("Image After", image)
    print(db)
    db.cards.insert_one({
        "id": id,
        "name": name,
        "image": image_id
    })
    return id

def get_card(id):
    card = db.cards.find_one({"id": id})
    return card

def get_card_image(id):
    fs = gridfs.GridFS(db)
    card_image_id = db.cards.find_one({"id": id})["image"]
    return fs.get(card_image_id).read()

card_id = add_card("MorphedCard", morphed_image)
#print("Card Test", get_card(card_id)["name"])
add_user("TestUsername", "TestPassword")
add_card_to_user("TestUsername", card_id)


image1 = bytes("https://www.cc.gatech.edu/sites/default/files/styles/profile_150x180_/public/images/profiles/2022-05/jacob_abernethy_0.png?itok=1FOhMTza".encode())
card_1 = add_card("Jacob Abernethy", image1)
add_card_to_user("TestUsername", card_1)
image2 = bytes("https://www.cc.gatech.edu/sites/default/files/styles/profile_150x180_/public/images/profiles/2022-05/joy_arulraj_0.png?itok=P7SALabz".encode())
card_2 = add_card("Joy Arulraj", image2)
add_card_to_user("TestUsername", card_2)
image3 = bytes("https://www.cc.gatech.edu/sites/default/files/styles/profile_150x180_/public/images/profiles/2022-01/gregory-abowd.jpg?itok=n9euLgCy".encode())
card_3 = add_card("Gregory Abowd", image3)
add_card_to_user("TestUsername", card_3)


#image1 = os.path.abspath("jacob_abernethy_0.png")
#image2 = os.path.abspath("joy_arulraj_0.png")
#morphed_image = automator.morph_image(image1, image2)
#return flask.render_template("scanQR.html")