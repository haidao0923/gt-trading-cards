from flask import Flask
import sqlite3

app = Flask(__name__)

#When a user scans the QR code for the card,
#this url opens up the card
#urls will be of the form:
#url, identifier  - which is primary key in the db
@app.route('/')
def home():
    #open the card, display the card
    return "Success"
if __name__ == '__main__':
    app.run()