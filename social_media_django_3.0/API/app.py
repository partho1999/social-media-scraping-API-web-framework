from turtle import left
from flask import Flask, render_template, request, send_file
from flask import jsonify
import requests
from functions import *
from pathlib import Path
import time
from io import BytesIO
import zipfile
import os
from flask import send_file



app = Flask(__name__)

@app.route('/',methods=['GET'])
def Home():
    return 'This is Homepage!'
    
@app.route("/username/<string:text>", methods=['GET','POST'])
def username(username):
    global user
    user=username
    return 1


@app.route("/google/<string:user>/<string:text>", methods=['GET','POST'])
def google(text,user):
    print('Key:',text)
    print('User:',user)
    try:
        df = Google(text,user)
        return df.to_json()
    except Exception as e:
        print(e)
        return 'Failed! Try Again..'

@app.route("/twitter/<string:user>/<string:text>", methods=['GET','POST'])
def twitter(text,user):
    print('Key:',text)
    print('User:',user)
    try:
        df = Twitter(500,text,user)
        
        return df.to_json()
    except Exception as e:
        print(e)
        return 'Failed! Try Again..'
    
# @app.route("/facebook_profile/<string:text>", methods=['GET','POST'])
# def facebook_profile(text):
#     print(text)
#     try:
#         df = Facebook(text) 
#         return df.to_json()
#     except:
#         return 'Failed! Try Again..'

@app.route("/facebook_posts/<string:user>/<string:text>", methods=['GET','POST'])
def facebook_posts(text,user):
    print('Key:',text)
    print('User:',user)
    try:
        df = Facebook(text,user) 
        
        return df.to_json()
        
    except Exception as e:
        print(e)
        df = Facebook_Posts(text,user)
        return df.to_json()
    
@app.route("/youtube/<string:user>/<string:text>", methods=['GET','POST'])
def youtube(text,user):
    print('Key:',text)
    print('User:',user)
    try:
        df = YouTube(text,user)
        return df.to_json()
    except Exception as e:
        
        print(e)
        return 'Failed! Try Again..'

@app.route('/facebook_posts/download/<string:text>')
def download_fb (text):
    #path =Path("C:\Users\Administrator\Documents\social_media_django_2.0\project\facebook_csv"+text)
    path = "C:/Users/Administrator/Documents/social_media_django_2.0/project/facebook_csv/"+text
    print(path)
    return send_file(path, as_attachment=True)
    
@app.route('/twitter/download/<string:text>')
def download_tw (text):
    path = r"C:/Users/Administrator/Documents/social_media_django_2.0/project/twitter_csv/"+text
    return send_file(path, as_attachment=True)
    
@app.route('/youtube/download/<string:text>')
def download_yt (text):
    path = r"C:/Users/Administrator/Documents/social_media_django_2.0/project/youtube_csv/"+text
    return send_file(path, as_attachment=True)
    
@app.route('/google/download/<string:text>')
def download_gl (text):
    path = r"C:/Users/Administrator/Documents/social_media_django_2.0/project/google_csv/"+text
    return send_file(path, as_attachment=True)

@app.route('/facebook_photo/download/<string:text>')
def download_img (text):
    fileName = "Facebook_Images_{}.zip".format(text)
    memory_file = BytesIO()
    file_path = r"C:/Users/Administrator/Documents/social_media_django_2.0/API/scrape_image/"+text
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
          for root, dirs, files in os.walk(file_path):
                    for file in files:
                              zipf.write(os.path.join(root, file))
    memory_file.seek(0)
    return send_file(memory_file,
                     attachment_filename=fileName,
                     as_attachment=True)




@app.route('/zipped_data')
def zipped_data():
    timestr = time.strftime("%Y%m%d-%H%M%S")
    fileName = "my_data_dump_{}.zip".format(timestr)
    memory_file = BytesIO()
    file_path = r"C:/Users/Administrator/Documents/social_media_django_2.0/API/scrape_image/"+text
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
          for root, dirs, files in os.walk(file_path):
                    for file in files:
                              zipf.write(os.path.join(root, file))
    memory_file.seek(0)
    return send_file(memory_file,
                     attachment_filename=fileName,
                     as_attachment=True)

    

    
        

    
if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0', port=1082)
