from turtle import left
from flask import Flask, render_template, request
from flask import jsonify
import requests
from functions import *

app = Flask(__name__)

@app.route('/',methods=['GET'])
def Home():
    return 'This is Homepage!'


@app.route("/google/<string:text>", methods=['GET','POST'])
def google(text):
    print(text)
    try:
        df = Google(text)
        return df.to_html()
    except:
        return 'Failed! Try Again..'

@app.route("/twitter/<string:text>", methods=['GET','POST'])
def twitter(text):
    print(text)
    try:
        df = Twitter(text)
        return df.to_html()
    except:
        return 'Failed! Try Again..'
    
@app.route("/facebook_profile/<string:text>", methods=['GET','POST'])
def facebook_profile(text):
    print(text)
    try:
        df = Facebook(text) 
        return df.to_html()
    except:
        return 'Failed! Try Again..'

@app.route("/facebook_posts/<string:text>", methods=['GET','POST'])
def facebook_posts(text):
    print(text)
    try:
        df = Facebook_Posts(text) 
        return df.to_html()
    except:
        return 'Failed! Try Again..'
    
@app.route("/youtube/<string:text>", methods=['GET','POST'])
def youtube(text):
    print(text)
    try:
        df = YouTube(text)
        return df.to_html()
    except:
        return 'Failed! Try Again..'
    

    
        

    
if __name__=="__main__":
    app.run(debug=True)