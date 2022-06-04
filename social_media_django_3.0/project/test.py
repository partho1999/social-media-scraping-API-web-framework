from turtle import left
from flask import Flask, render_template, request, send_file
from flask import jsonify
import requests
from functions import *


app = Flask(__name__)

@app.route('/',methods=['GET'])
def Home():
    return 'This is Homepage!'
    
@app.route("/username/<string:text>", methods=['GET','POST'])
def username(username):
    global user
    user=username
    return 1


@app.route("/google/<string:text>", methods=['GET','POST'])
def google(text):
    print(text)
    try:
        df = Google(text)
        return df.to_html()
    except:
        return 'Failed! Try Again..'

@app.route("/twitter/<string:user>/<string:text>", methods=['GET','POST'])
def twitter(text,user):
    print('Key:',text)
    print('User:',user)
    try:
        df = Twitter(text,user)
        return df.to_html()
    except Exception as e:
        print(e)
        return 'Failed! Try Again..'
    
@app.route("/facebook_profile/<string:text>", methods=['GET','POST'])
def facebook_profile(text):
    print(text)
    try:
        df = Facebook(text) 
        return df.to_html()
    except:
        return 'Failed! Try Again..'

@app.route("/facebook_posts/<string:user>/<string:text>", methods=['GET','POST'])
def facebook_posts(text,user):
    print('Key:',text)
    print('User:',user)
    try:
        df = Facebook_Posts(text,user)
        return df.to_html()
    except Exception as e:
        print(e)
        return 'Failed! Try Again..'
    
@app.route("/youtube/<string:text>", methods=['GET','POST'])
def youtube(text):
    print(text)
    try:
        df = YouTube(text)
        return df.to_html()
    except:
        return 'Failed! Try Again..'

@app.route('/facebook_posts/download/<string:text>')
def download_fb (text):
    path = "/home/opus/Desktop/social_media_dj/project/facebook_csv/"+text
    return send_file(path, as_attachment=True)
    
@app.route('/twitter/download/<string:text>')
def download_tw (text):
    path = "/home/opus/Desktop/social_media_dj/project/twitter_csv/"+text
    return send_file(path, as_attachment=True)
    
@app.route('/youtube/download/<string:text>')
def download_yt (text):
    path = "/home/opus/Desktop/social_media_dj/project/youtube_csv/"+text
    return send_file(path, as_attachment=True)
    
@app.route('/google/download/<string:text>')
def download_gl (text):
    path = "/home/opus/Desktop/social_media_dj/project/google_csv/"+text
    return send_file(path, as_attachment=True)
    
    
    
    

    
        

    
if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)