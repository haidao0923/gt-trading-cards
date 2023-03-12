from flask import Flask, request, jsonify, redirect, url_for
import flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Placeholder"
    #open the card, display the card
@app.route("/test")
def test():
    return flask.render_template_string("HI")

#url paramter here has 1'st card
@app.route('/qrResponse', methods = ["POST", "GET"])
def qr_response():
    #get qr code response, tell the client to scan the next card
    if request.method == "POST":
        #this is the second card. The id is contained in the response
        id1 = request.get_json()['id1']
        id2 = request.get_json()['id2']

        #send both of these to be merged, and return the result to client

        return "Hi"

    else: #user just scanned the FIRST card
        #get the identifier of the FIRST card from url
        return flask.render_template("scanQR.html")


if __name__ == '__main__':
    app.run()