from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import pymongo
import gridfs
import json

with open("config.json", 'r') as f:
    config = json.load(f)
print(config['mongoDBURI'])

chrome_options = Options()
chrome_options.add_argument("--headless")

def morph_image(image1, image2):
    driver = webdriver.Chrome('C:/Users/haixd/AppData/Local/Programs/Python/Python36-32/Scripts/chromedriver', options=chrome_options)
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


image1 = "jacob_abernethy_0.png"
image2 = "joy_arulraj_0.png"
morphed_image = morph_image(image1, image2)


client = pymongo.MongoClient(config['mongoDBURI'])
db = client.gttc

def add_user(username, password):
    db.users.insert_one({
        "username": username,
        "password": password
    })

def add_card(name, image):
    fs = gridfs.GridFS(db)
    #print("Image Before", morphed_image)
    id = fs.put(morphed_image)
    image = fs.get(id).read()
    #print("Image After", image)
    print(db)
    db.cards.insert_one({
        "id": 0,
        "name": "Jacob Abernethy",
        "image": id
    })


def get_card(id):
    id_query = {"id": id}
    card = db.cards.find(id_query)
    return card

add_card("MorphedCard", morphed_image)
print(get_card(0))

add_user("TestUsername", "TestPassword")