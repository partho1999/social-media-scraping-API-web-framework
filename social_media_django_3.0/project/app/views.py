from ast import Return, dump
from datetime import date
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from matplotlib.style import context
from .models import UserProfile
from django.core.files.storage import FileSystemStorage
from project import settings
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
import os
import json
import pandas as pd
from wordcloud import WordCloud
from analysis import *
from word_cloud import *
import urllib, json
import urllib.parse
from nltk import tokenize
from operator import itemgetter
import math
import sys
import nltk
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
stop_words = nltk.corpus.stopwords.words('english')
new_stop_words = ['?', 'the', '.', ',','--','we', 'us', 'i', 'our', 'We', 'Our']
stop_words.extend(new_stop_words)

# from functions import *

search_word=[]

# Create your views here.
def index(request):
    # return HttpResponse("this is home Page...!!!")
    return render(request, 'index.html')

def user_register(request):
    if request.method=='POST':
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if pass1 != pass2:
            messages.warning(request, 'Password does not match...!')
            return redirect('register')

        elif User.objects.filter(username=uname).exists():
            messages.warning(request, 'This username already exists')
            return redirect('register')

        elif User.objects.filter(email=email).exists():
            messages.warning(request, 'This email already exists')
            return redirect('register')
        
        else:
            #print(fname,lname,uname,email,pass1,pass2)
            user = User.objects.create_user(first_name=fname, last_name=lname, username=uname, email=email, password=pass1)
            user.first_name = fname
            user.last_name = lname
            user.is_active = False
            user.save()
            messages.success(request,'You have been registered succssfully! Please check your email to confirm your email address in order to activate your account.')

            # Welcome Email
            subject = "Welcome to Opus Scraper website...!!!"
            message = "Hello " + user.first_name + "!! \n" + "Welcome to Opus Scraper!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nOpus Technology Limited"        
            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
            
            # Email Address Confirmation Email
            current_site = get_current_site(request)
            email_subject = "Confirm your Email @ Opus Scraper Login!!"
            message2 = render_to_string('email_confirmation.html',{
                
                'name': user.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            })
            email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [user.email],
            )
            email.fail_silently = True
            email.send()

            return redirect('login')
    return render(request,'register.html')


def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user,token):
        user.is_active = True
        # user.profile.signup_confirmation = True
        user.save()
        login(request,user)
        messages.success(request, "Your Account has been activated!!")
        return redirect('login')
    else:
        return render(request,'activation_failed.html')
    

def user_login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('social')
        else:
            messages.warning(request, 'invalid value! Please register first or try again...')
            return redirect('login')
    return render(request,'login.html')

def user_logout(request):
    logout(request)
    return redirect('/')

@login_required
def social(request):
    return render(request, 'social.html')

@login_required
def facebook_search (request):
    def fun():
        global username
        try:
            print("Yay! I still got executed, even though my function has already returned!.... facebook")
        finally:

            

            #defines what happens when there is a POST request
            if request.method == "POST":
                title = (request.POST.get("q"))
                print(title)
                # title= title.encode('utf-8', errors='ignore')
                title = u' '+title
                title = title.strip()
                search_word = word_tokenize(title)
                stop_words.extend(search_word)
                # title = title.replace(" ", "%20").strip()
                print(title)
                # print(title)
                # print(request.user.username)
                title=urllib.parse.quote(title)
                username = request.user.username
                # url1='http://103.101.197.155:1082/username/'+username
                # res = HttpResponseRedirect(url1)

                url ='http://103.101.197.155:1082/facebook_posts/' +username+'/'+title
                # print(url)

                # df = Facebook_Posts(title)
                # url = df.to_html()
                #return HttpResponseRedirect(url)
                # return render(request,'result.html', { 'url' : url })
                print(url)
                response = urllib.request.urlopen(url)
                print('Got Response!')
                data =[]
                data = json.loads(response.read())
                #print (data)
                df = pd.json_normalize(data,max_level=0)
                print(df)
                tmp=pd.DataFrame()
                for name in df.columns:
                    values=df[name][0].values()
                    tmp[name]=values
                

                if "Post" in tmp.columns:
                    print ("hello from fb post") 
                    pst_path =tmp.iloc[0]['file_path']
                    pst_d_link = 'http://103.101.197.155:1082/facebook_posts/download/' + pst_path
                    pst_img_d_link = 'http://103.101.197.155:1082/facebook_photo/download/' + title
                    tmp['SL']=list(range(1,len(tmp)+1)) 
                    json_records = tmp.reset_index().to_json(orient ='records')
                    data_4 = []
                    data_4 = json.loads(json_records)
                    context = {'f': data_4}
                    context['pst_link'] = pst_d_link
                    context['pst_img_d_link'] =pst_img_d_link
                    context['keyword'] = title
                    return render(request,'facebook_post_tb.html',context)
                else:
                    print("hello from fb profile..")
                    post_path =tmp.iloc[0]['Post_Path']
                    post_d_link = 'http://103.101.197.155:1082/facebook_posts/download/' + post_path
                    pro_img_d_link = 'http://103.101.197.155:1082/facebook_photo/download/' + title
                    Post_df = tmp[['ID_Name', 'Pro_Posts','img_link']]
                    Post_df ['SL']=list(range(1,len(Post_df)+1)) 
                    json_records = Post_df.reset_index().to_json(orient ='records')
                    data_9 = []
                    data_9 = json.loads(json_records)

                    tmp=tmp.drop(['ID_Name', 'Pro_Posts', 'Post_Path', 'img_link'], axis=1)[:1]
                    pro_path =tmp.iloc[0]['pro_path']
                    pro_d_link = 'http://103.101.197.155:1082/facebook_posts/download/' + pro_path
                    ind = tmp.columns.tolist()
                    val = tmp.values.flatten().tolist()

                    df = pd.DataFrame({
                        "index": ind,
                        "values": val,
                    })
                    df['SL']=list(range(1,len(df)+1)) 
                    json_records = df.reset_index().to_json(orient ='records')
                    data_4 = []
                    data_4 = json.loads(json_records)
                    context = {'f': data_4, 'j': data_9}
                    context['post_link'] = post_d_link
                    context['pro_link'] = pro_d_link
                    context['pro_img_d_link'] = pro_img_d_link
                    context['keyword'] = title
                    
                    return render(request,'facebook_profile_tb.html',context)

                    

            #defines what happens when there is a GET request
            else:
                return render(request,'fb_search.html')

    return fun()




@login_required
def twitter_search (request):
    def fun():
        try:
            print("Yay! I still got executed, even though my function has already returned!...  twitter")
        finally:

            

            #defines what happens when there is a POST request
            if request.method == "POST":
                title = request.POST.get("q")
                search_word = word_tokenize(title)
                stop_words.extend(search_word)
                title = title.replace(" ", "%20")
                print(title)
                username = request.user.username

                url ='http://103.101.197.155:1082/twitter/' +username+'/'+title
                #return HttpResponseRedirect(url)
                # df = Twitter(title)
                # url = df.to_html()
                # print(url)
               
                # return render(request,'result.html', { 'url' : url })

                response = urllib.request.urlopen(url)
                data =[]
                data = json.loads(response.read())
                #print (data)
                df = pd.json_normalize(data,max_level=0)
                print(df)
                tmp=pd.DataFrame()
                for name in df.columns:
                    values=df[name][0].values()
                    tmp[name]=values
                file_name = tmp.iloc[0]['file_path']
                d_link ='http://103.101.197.155:1082/twitter/download/' +file_name
                tmp['SL']=list(range(1,len(tmp.Post)+1))

                json_records = tmp.reset_index().to_json(orient ='records')
                data_4 = []
                data_4 = json.loads(json_records)
                context = {'f': data_4}
                context['download_link'] = d_link
                return render(request,'twitter_result_tb.html',context)



            #defines what happens when there is a GET request
            else:
                return render(request,'tw_search.html')

    return fun()

@login_required
def twitter_download(request):
    url = 'http://103.101.197.155:1082/twitter/download'
    return HttpResponseRedirect(url)


@login_required
def youtube_search (request):
    def fun():
        try:
            print("Yay! I still got executed, even though my function has already returned!...  youtube")
        finally:

            

            #defines what happens when there is a POST request
            if request.method == "POST":
                title = request.POST.get("q")
                search_word = word_tokenize(title)
                stop_words.extend(search_word)
                title = title.replace(" ", "%20")
                print(title)
                username = request.user.username

                url ='http://103.101.197.155:1082/youtube/' +username+'/'+title
                #return HttpResponseRedirect(url)
                # print(url)
                # return render(request,'result.html', { 'url' : url })
                response = urllib.request.urlopen(url)
                data =[]
                data = json.loads(response.read())
                #print (data)
                df = pd.json_normalize(data,max_level=0)
                print(df)
                tmp=pd.DataFrame()
                for name in df.columns:
                    values=df[name][0].values()
                    tmp[name]=values
                file_name = tmp.iloc[0]['file_path']
                d_link ='http://103.101.197.155:1082/youtube/download/' +file_name
                tmp['SL']=list(range(1,len(tmp)+1)) 

                
                json_records = tmp.reset_index().to_json(orient ='records')
                data_4 = []
                data_4 = json.loads(json_records)
                context = {'f': data_4}
                context['download_link'] = d_link
                return render(request,'youtube_result_tb.html',context)




            #defines what happens when there is a GET request
            else:
                return render(request,'yt_search.html')

    return fun()

@login_required
def youtube_download(request):
    url = 'http://103.101.197.155:1082/youtube/download'
    return HttpResponseRedirect(url)

@login_required
def google_search (request):
    def fun():
        try:
            print("Yay! I still got executed, even though my function has already returned!... google")
        finally:

            

            #defines what happens when there is a POST request
            if request.method == "POST":
                title = request.POST.get("q")
                print(title)
                search_word = word_tokenize(title)
                stop_words.extend(search_word)
                title = title.replace(" ", "%20")
                username = request.user.username

                url ='http://103.101.197.155:1082/google/'+username+'/'+title
                #return HttpResponseRedirect(url)
                #print(url)

                # return render(request,'result.html', { 'url' : url })
                
                #url = "http://103.101.197.155:1082/google/partho/bangladesh"
                response = urllib.request.urlopen(url)
                data =[]
                data = json.loads(response.read())
                #print (data)
                df = pd.json_normalize(data,max_level=0)
                print(df)
                tmp=pd.DataFrame()
                for name in df.columns:
                    values=df[name][0].values()
                    tmp[name]=values

                tmp['datetime']=pd.to_datetime(tmp.datetime, utc=True, unit='ms')
                tmp = tmp.sort_values(by="media", ascending=False)
                file_name = tmp.iloc[0]['file_path']
                d_link ='http://103.101.197.155:1082/google/download/' +file_name

                tmp['SL']=list(range(1,len(tmp.Post)+1)) 



                json_records = tmp.reset_index().to_json(orient ='records')
                data_3 = []
                data_3 = json.loads(json_records)



                context = {'f': data_3}
                context['download_link'] = d_link
                #print(context)

                return render(request,'google_result_tb.html',context)


            #defines what happens when there is a GET request
            else:
                return render(request,'gl_search.html')

    return fun()

@login_required
def google_download(request):
    url = 'http://103.101.197.155:1082/google/download'
    return HttpResponseRedirect(url)

# def upload_file(request):
    
#     if request.method == 'POST':

#         uploaded_file = request.FILES['document']
#         print(uploaded_file)

#         if uploaded_file.name.endswith('.csv'):
            
#             savefile = FileSystemStorage()
#             #we need to save the file somewhere in the project, MEDIA
#             #now lets do the savings
#             uploaded_file_name = "facebook_post.csv"
#             if os.path.exists('media/facebook_post.csv'):
#                 print ("File exist")
#                 os.remove('media/facebook_post.csv')
#                 print('Existing File Removed!')
#             name = savefile.save(uploaded_file_name, uploaded_file) #gets the name of the file
#             print(name)

#             d = os.getcwd() # how we get the current dorectory
#             file_directory = d+'\media\\'+name #saving the file in the media directory
#             print(file_directory) 
#             text_analysis() 
#             readFile('media/analysis.csv')
#             #messages.success(request, 'your file is uploaded succssfully!')
#             return redirect('dashboard')

#         else:
#             messages.success(request, 'your file is not uploaded!')


#     else:
#         pass
#         #messages.warning(request, 'File was not uploaded. Please use .csv file extension!')


#     return render(request, 'upload_file.html')

# def readFile(filename):
#    global rows, columns, data, my_file, missing_values

#    missingvalue = ['?', '0', '--'] 
#    my_file = pd.read_csv(filename, sep=',',na_values=missingvalue, engine='python') 
#    data = pd.DataFrame(data=my_file, index=None)
#    data = data.fillna(0)
#    print(data)

#    rows = len(data.axes[0])
#    columns = len(data.axes[1])
   
#    null_data = data[data.isnull().any(axis=1)] # find where is the missing data #na null =['x1','x13']
#    missing_values = len(null_data)

@login_required
def fb_dashboard(request,path):
    df = pd.read_csv('facebook_csv/'+path)
    #df.shape[0]

    corpus=[]

    for i in range(0, df.shape[0]):
        post = re.sub('(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)|([^0-9A-Za-z t])|(w+://S+)', ' ', str(df['Post'][i]))
        post = post.split("https")[0]
        post = post.lower()
        post = post.split()
        post = [ps.stem(word) for word in post if not word in set(all_stopwords)]
        post = ' '.join(post)
        corpus.append(post)


    df['text'] = corpus

    df['scores'] = df['text'].apply(lambda Text: sid.polarity_scores(Text))

    df = df[['Post','scores']]

    df = pd.concat([df, df['scores'].apply(pd.Series)], axis=1)

    df = df[['Post','neg', 'neu', 'pos', 'compound']]

    df.to_csv("media/analysis.csv")

    missingvalue = ['?', '0', '--'] 
    my_file = pd.read_csv('media/analysis.csv', sep=',',na_values=missingvalue, engine='python') 
    data = pd.DataFrame(data=my_file, index=None)
    data = data.fillna(0)
    print(data)

    rows = len(data.axes[0])
    columns = len(data.axes[1])
    
    null_data = data[data.isnull().any(axis=1)] # find where is the missing data #na null =['x1','x13']
    missing_values = len(null_data)


    message = 'I found ' + str(rows) + ' rows and ' + str(columns) + ' columns. Missing data: ' + str(missing_values)
    messages.warning(request, message)

    data.isna().sum()
    #Removing NaN Values
    data.dropna(inplace = True)


    neg_avg = data["neg"].mean()
    neu_avg = data["neu"].mean()
    pos_avg = data["pos"].mean()
    
    
    pos_avg = 0.9 - neg_avg
    neg_avg = 0.9 - pos_avg
    neu_avg = 1 - (neg_avg + pos_avg)
    

    avg =[neg_avg, neu_avg, pos_avg]
    print(avg)

    word_cloud()


    #2. Loading Data
    doc_csv = pd.read_csv('media/analysis.csv')
    #take it to list
    doc_list = doc_csv['Post'].tolist()
    #print(doc_list)
    #Convert Data list to str
    doc = ''.join(str(e) for e in doc_list)

    #3. Remove stopwords
    #4. Find total words in the document 
    total_words = doc.split()
    total_word_length = len(total_words)
    #print(total_word_length)

    #5. Find the total number of sentences
    total_sentences = tokenize.sent_tokenize(doc)
    total_sent_len = len(total_sentences)
    #print(total_sent_len)

    #6. Calculate TF for each word
    tf_score = {}
    for each_word in total_words:
        each_word = each_word.replace('.','')
        each_word = re.sub('(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)|([^0-9A-Za-z t])|(w+://S+)', ' ', each_word)
        each_word = re.sub(r'[0-9]+', '', each_word)
        if each_word not in stop_words:
            if each_word in tf_score:
                tf_score[each_word] += 1
            else:
                tf_score[each_word] = 1

    # Dividing by total_word_length for each dictionary element
    tf_score.update((x, y/int(total_word_length)) for x, y in tf_score.items())
    #print(tf_score)

    #7. Function to check if the word is present in a sentence list
    def check_sent(word, sentences): 
        final = [all([w in x for w in word]) for x in sentences] 
        sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
        return int(len(sent_len))

    #8. Calculate IDF for each word
    idf_score = {}
    for each_word in total_words:
        each_word = each_word.replace('.','')
        if each_word not in stop_words:
            if each_word in idf_score:
                idf_score[each_word] = check_sent(each_word, total_sentences)
            else:
                idf_score[each_word] = 1

    # Performing a log and divide
    idf_score.update((x, math.log(int(total_sent_len)/y)) for x, y in idf_score.items())

    #print(idf_score)

    #9. Calculate TF * IDF
    tf_idf_score = {key: tf_score[key] * idf_score.get(key, 0) for key in tf_score.keys()}
    #print(tf_idf_score)

    #10. Create a function to get N important words in the document
    def get_top_n(dict_elem, n):
        result = dict(sorted(dict_elem.items(), key = itemgetter(1), reverse = True)[:n]) 
        return result
    #11. Get the top 5 words of significance
    print(get_top_n(tf_idf_score, 10))

    dic = get_top_n(tf_idf_score, 10)

    df=pd.DataFrame()
    df['Keyword']=dic.keys()
    df['Score']=dic.values()

    #print(df)

    df_label = df['Keyword'].tolist()
    df_score = df['Score'].tolist()

    print(df_label)
    print(df_score)    
    
    
   
    return render(request, 'dashboard.html', context={'avg' : avg,'df_label':df_label,'df_score':df_score})

@login_required
def tw_dashboard(request,path):
    df = pd.read_csv('twitter_csv/'+path)
    #df.shape[0]

    corpus=[]

    for i in range(0, df.shape[0]):
        post = re.sub('(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)|([^0-9A-Za-z t])|(w+://S+)', ' ', str(df['Post'][i]))
        post = post.split("https")[0]
        post = post.lower()
        post = post.split()
        post = [ps.stem(word) for word in post if not word in set(all_stopwords)]
        post = ' '.join(post)
        corpus.append(post)


    df['text'] = corpus

    df['scores'] = df['text'].apply(lambda Text: sid.polarity_scores(Text))

    df = df[['Post','scores']]

    df = pd.concat([df, df['scores'].apply(pd.Series)], axis=1)

    df = df[['Post','neg', 'neu', 'pos', 'compound']]

    df.to_csv("media/analysis.csv")

    missingvalue = ['?', '0', '--'] 
    my_file = pd.read_csv('media/analysis.csv', sep=',',na_values=missingvalue, engine='python') 
    data = pd.DataFrame(data=my_file, index=None)
    data = data.fillna(0)
    print(data)

    rows = len(data.axes[0])
    columns = len(data.axes[1])
    
    null_data = data[data.isnull().any(axis=1)] # find where is the missing data #na null =['x1','x13']
    missing_values = len(null_data)


    message = 'I found ' + str(rows) + ' rows and ' + str(columns) + ' columns. Missing data: ' + str(missing_values)
    messages.warning(request, message)

    data.isna().sum()
    #Removing NaN Values
    data.dropna(inplace = True)


    neg_avg = data["neg"].mean()
    neu_avg = data["neu"].mean()
    pos_avg = data["pos"].mean()

        
    pos_avg = 0.9 - neg_avg
    neg_avg = 0.9 - pos_avg
    neu_avg = 1 - (neg_avg + pos_avg)
    

    avg =[neg_avg, neu_avg, pos_avg]
    print(avg)

    word_cloud()


    #2. Loading Data
    doc_csv = pd.read_csv('media/analysis.csv')
    #take it to list
    doc_list = doc_csv['Post'].tolist()
    #print(doc_list)
    #Convert Data list to str
    doc = ''.join(str(e) for e in doc_list)

    #3. Remove stopwords
    #4. Find total words in the document 
    total_words = doc.split()
    total_word_length = len(total_words)
    #print(total_word_length)

    #5. Find the total number of sentences
    total_sentences = tokenize.sent_tokenize(doc)
    total_sent_len = len(total_sentences)
    #print(total_sent_len)

    #6. Calculate TF for each word
    tf_score = {}
    for each_word in total_words:
        each_word = each_word.replace('.','')
        each_word = re.sub('(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)|([^0-9A-Za-z t])|(w+://S+)', ' ', each_word)
        each_word = re.sub(r'[0-9]+', '', each_word)
        if each_word not in stop_words:
            if each_word in tf_score:
                tf_score[each_word] += 1
            else:
                tf_score[each_word] = 1

    # Dividing by total_word_length for each dictionary element
    tf_score.update((x, y/int(total_word_length)) for x, y in tf_score.items())
    #print(tf_score)

    #7. Function to check if the word is present in a sentence list
    def check_sent(word, sentences): 
        final = [all([w in x for w in word]) for x in sentences] 
        sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
        return int(len(sent_len))

    #8. Calculate IDF for each word
    idf_score = {}
    for each_word in total_words:
        each_word = each_word.replace('.','')
        if each_word not in stop_words:
            if each_word in idf_score:
                idf_score[each_word] = check_sent(each_word, total_sentences)
            else:
                idf_score[each_word] = 1

    # Performing a log and divide
    idf_score.update((x, math.log(int(total_sent_len)/y)) for x, y in idf_score.items())

    #print(idf_score)

    #9. Calculate TF * IDF
    tf_idf_score = {key: tf_score[key] * idf_score.get(key, 0) for key in tf_score.keys()}
    #print(tf_idf_score)

    #10. Create a function to get N important words in the document
    def get_top_n(dict_elem, n):
        result = dict(sorted(dict_elem.items(), key = itemgetter(1), reverse = True)[:n]) 
        return result
    #11. Get the top 5 words of significance
    print(get_top_n(tf_idf_score, 10))

    dic = get_top_n(tf_idf_score, 10)

    df=pd.DataFrame()
    df['Keyword']=dic.keys()
    df['Score']=dic.values()

    #print(df)

    df_label = df['Keyword'].tolist()
    df_score = df['Score'].tolist()

    print(df_label)
    print(df_score)    
    
    
   
    return render(request, 'dashboard.html', context={'avg' : avg,'df_label':df_label,'df_score':df_score})

@login_required
def gl_dashboard(request,path):
    df = pd.read_csv('google_csv/'+path)
    #df.shape[0]

    corpus=[]

    for i in range(0, df.shape[0]):
        post = re.sub('(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)|([^0-9A-Za-z t])|(w+://S+)', ' ', str(df['Post'][i]))
        post = post.split("https")[0]
        post = post.lower()
        post = post.split()
        post = [ps.stem(word) for word in post if not word in set(all_stopwords)]
        post = ' '.join(post)
        corpus.append(post)


    df['text'] = corpus

    df['scores'] = df['text'].apply(lambda Text: sid.polarity_scores(Text))

    df = df[['Post','scores']]

    df = pd.concat([df, df['scores'].apply(pd.Series)], axis=1)

    df = df[['Post','neg', 'neu', 'pos', 'compound']]

    df.to_csv("media/analysis.csv")

    missingvalue = ['?', '0', '--'] 
    my_file = pd.read_csv('media/analysis.csv', sep=',',na_values=missingvalue, engine='python') 
    data = pd.DataFrame(data=my_file, index=None)
    data = data.fillna(0)
    print(data)

    rows = len(data.axes[0])
    columns = len(data.axes[1])
    
    null_data = data[data.isnull().any(axis=1)] # find where is the missing data #na null =['x1','x13']
    missing_values = len(null_data)


    message = 'I found ' + str(rows) + ' rows and ' + str(columns) + ' columns. Missing data: ' + str(missing_values)
    messages.warning(request, message)

    data.isna().sum()
    #Removing NaN Values
    data.dropna(inplace = True)


    neg_avg = data["neg"].mean()
    neu_avg = data["neu"].mean()
    pos_avg = data["pos"].mean()

        
    pos_avg = 0.9 - neg_avg
    neg_avg = 0.9 - pos_avg
    neu_avg = 1 - (neg_avg + pos_avg)
    

    avg =[neg_avg, neu_avg, pos_avg]
    print(avg)

    word_cloud()


    #2. Loading Data
    doc_csv = pd.read_csv('media/analysis.csv')
    #take it to list
    doc_list = doc_csv['Post'].tolist()
    #print(doc_list)
    #Convert Data list to str
    doc = ''.join(str(e) for e in doc_list)

    #3. Remove stopwords
    #4. Find total words in the document 
    total_words = doc.split()
    total_word_length = len(total_words)
    #print(total_word_length)

    #5. Find the total number of sentences
    total_sentences = tokenize.sent_tokenize(doc)
    total_sent_len = len(total_sentences)
    #print(total_sent_len)

    #6. Calculate TF for each word
    tf_score = {}
    for each_word in total_words:
        each_word = each_word.replace('.','')
        each_word = re.sub('(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)|([^0-9A-Za-z t])|(w+://S+)', ' ', each_word)
        each_word = re.sub(r'[0-9]+', '', each_word)
        if each_word not in stop_words:
            if each_word in tf_score:
                tf_score[each_word] += 1
            else:
                tf_score[each_word] = 1

    # Dividing by total_word_length for each dictionary element
    tf_score.update((x, y/int(total_word_length)) for x, y in tf_score.items())
    #print(tf_score)

    #7. Function to check if the word is present in a sentence list
    def check_sent(word, sentences): 
        final = [all([w in x for w in word]) for x in sentences] 
        sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
        return int(len(sent_len))

    #8. Calculate IDF for each word
    idf_score = {}
    for each_word in total_words:
        each_word = each_word.replace('.','')
        if each_word not in stop_words:
            if each_word in idf_score:
                idf_score[each_word] = check_sent(each_word, total_sentences)
            else:
                idf_score[each_word] = 1

    # Performing a log and divide
    idf_score.update((x, math.log(int(total_sent_len)/y)) for x, y in idf_score.items())

    #print(idf_score)

    #9. Calculate TF * IDF
    tf_idf_score = {key: tf_score[key] * idf_score.get(key, 0) for key in tf_score.keys()}
    #print(tf_idf_score)

    #10. Create a function to get N important words in the document
    def get_top_n(dict_elem, n):
        result = dict(sorted(dict_elem.items(), key = itemgetter(1), reverse = True)[:n]) 
        return result
    #11. Get the top 5 words of significance
    print(get_top_n(tf_idf_score, 10))

    dic = get_top_n(tf_idf_score, 10)

    df=pd.DataFrame()
    df['Keyword']=dic.keys()
    df['Score']=dic.values()

    #print(df)

    df_label = df['Keyword'].tolist()
    df_score = df['Score'].tolist()

    print(df_label)
    print(df_score)    
    
    
   
    return render(request, 'dashboard.html', context={'avg' : avg,'df_label':df_label,'df_score':df_score})

@login_required
def yt_dashboard(request,path):
    df = pd.read_csv('youtube_csv/'+path)
    #df.shape[0]

    corpus=[]

    for i in range(0, df.shape[0]):
        post = re.sub('(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)|([^0-9A-Za-z t])|(w+://S+)', ' ', str(df['Post'][i]))
        post = post.split("https")[0]
        post = post.lower()
        post = post.split()
        post = [ps.stem(word) for word in post if not word in set(all_stopwords)]
        post = ' '.join(post)
        corpus.append(post)


    df['text'] = corpus

    df['scores'] = df['text'].apply(lambda Text: sid.polarity_scores(Text))

    df = df[['Post','scores']]

    df = pd.concat([df, df['scores'].apply(pd.Series)], axis=1)

    df = df[['Post','neg', 'neu', 'pos', 'compound']]

    df.to_csv("media/analysis.csv")

    missingvalue = ['?', '0', '--'] 
    my_file = pd.read_csv('media/analysis.csv', sep=',',na_values=missingvalue, engine='python') 
    data = pd.DataFrame(data=my_file, index=None)
    data = data.fillna(0)
    print(data)

    rows = len(data.axes[0])
    columns = len(data.axes[1])
    
    null_data = data[data.isnull().any(axis=1)] # find where is the missing data #na null =['x1','x13']
    missing_values = len(null_data)


    message = 'I found ' + str(rows) + ' rows and ' + str(columns) + ' columns. Missing data: ' + str(missing_values)
    messages.warning(request, message)

    data.isna().sum()
    #Removing NaN Values
    data.dropna(inplace = True)


    neg_avg = data["neg"].mean()
    neu_avg = data["neu"].mean()
    pos_avg = data["pos"].mean()

        
    pos_avg = 0.9 - neg_avg
    neg_avg = 0.9 - pos_avg
    neu_avg = 1 - (neg_avg + pos_avg)
    
    avg =[neg_avg, neu_avg, pos_avg]
    print(avg)

    word_cloud()


    #2. Loading Data
    doc_csv = pd.read_csv('media/analysis.csv')
    #take it to list
    doc_list = doc_csv['Post'].tolist()
    #print(doc_list)
    #Convert Data list to str
    doc = ''.join(str(e) for e in doc_list)

    #3. Remove stopwords
    #4. Find total words in the document 
    total_words = doc.split()
    total_word_length = len(total_words)
    #print(total_word_length)

    #5. Find the total number of sentences
    total_sentences = tokenize.sent_tokenize(doc)
    total_sent_len = len(total_sentences)
    #print(total_sent_len)

    #6. Calculate TF for each word
    tf_score = {}
    for each_word in total_words:
        each_word = each_word.replace('.','')
        each_word = re.sub('(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)|([^0-9A-Za-z t])|(w+://S+)', ' ', each_word)
        each_word = re.sub(r'[0-9]+', '', each_word)
        if each_word not in stop_words:
            if each_word in tf_score:
                tf_score[each_word] += 1
            else:
                tf_score[each_word] = 1

    # Dividing by total_word_length for each dictionary element
    tf_score.update((x, y/int(total_word_length)) for x, y in tf_score.items())
    #print(tf_score)

    #7. Function to check if the word is present in a sentence list
    def check_sent(word, sentences): 
        final = [all([w in x for w in word]) for x in sentences] 
        sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
        return int(len(sent_len))

    #8. Calculate IDF for each word
    idf_score = {}
    for each_word in total_words:
        each_word = each_word.replace('.','')
        if each_word not in stop_words:
            if each_word in idf_score:
                idf_score[each_word] = check_sent(each_word, total_sentences)
            else:
                idf_score[each_word] = 1

    # Performing a log and divide
    idf_score.update((x, math.log(int(total_sent_len)/y)) for x, y in idf_score.items())

    #print(idf_score)

    #9. Calculate TF * IDF
    tf_idf_score = {key: tf_score[key] * idf_score.get(key, 0) for key in tf_score.keys()}
    #print(tf_idf_score)

    #10. Create a function to get N important words in the document
    def get_top_n(dict_elem, n):
        result = dict(sorted(dict_elem.items(), key = itemgetter(1), reverse = True)[:n]) 
        return result
    #11. Get the top 5 words of significance
    print(get_top_n(tf_idf_score, 10))

    dic = get_top_n(tf_idf_score, 10)

    df=pd.DataFrame()
    df['Keyword']=dic.keys()
    df['Score']=dic.values()

    #print(df)

    df_label = df['Keyword'].tolist()
    df_score = df['Score'].tolist()

    print(df_label)
    print(df_score)    
    
    
   
    return render(request, 'dashboard.html', context={'avg' : avg,'df_label':df_label,'df_score':df_score})



@login_required
def user_profile(request, user_id):
	if request.method == 'POST':
		user_obj = User.objects.get(id=user_id)
		user_profile_obj = UserProfile.objects.get(id=user_id)
		# try:
		user_img = request.FILES['user_img']
		fs_handle = FileSystemStorage()
		img_name = 'images/user_{0}.png'.format(user_id)
		if fs_handle.exists(img_name):
			fs_handle.delete(img_name)
		fs_handle.save(img_name, user_img)
		user_profile_obj.profile_img = img_name
		user_profile_obj.save()
		user_profile_obj.refresh_from_db()
		# except:
		# 	messages.add_message(request, messages.ERROR, "Unable to update image..")

		return render(request, 'profile.html', {'my_profile': user_profile_obj})
	if (request.user.is_authenticated and request.user.id == user_id):
		user_obj = User.objects.get(id=user_id)
		user_profile = UserProfile.objects.get(id=user_id)

		return render(request, 'profile.html', {'my_profile': user_profile})

    

def download(request):
    #For Facebook
    current_site = get_current_site(request)
    print(current_site.domain)

    # Get the list of all files and directories
    path = "facebook_csv/"
    dir_list = os.listdir(path)
    
    print("Files and directories in '", path, "' :")
    
    # prints all files
    #print(dir_list)
     
    username = request.user.username
    #print(username)
    filtered_lst=[]
    for element in dir_list:
        if username in element:
            filtered_lst.append(element)

    #print filtered file
    print(filtered_lst)

    dates =[]
    times =[]
    keywords =[]
    link = []
    path = []


    for file in filtered_lst:
        date = file.split("-")[0].replace('_','/')
        dates.append(date)
        time = file.split("-")[1].replace('_',':')
        times.append(time)
        keyword= file.split("-")[2]
        keywords.append(keyword)
        downloadpath = file
        print("path:",downloadpath)
        path.append('/'+'fb_dashbaord/'+downloadpath)
        link.append('http://103.101.197.155:1082/facebook_posts/download/' +file)
        print('http://103.101.197.155:1082/facebook_posts/download/' +file)

    print(dates, times, keywords, link)
    sl=list(range(1,len(keywords)+1)) 
    print(sl)   

    
    
    df = pd.DataFrame(
    {'SL' : sl,
     'keywords' : keywords,
     'times':times,
     'dates':dates,
     'link' :link,
     'path' :path
    })
    print(df)  
    json_records = df.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)

################################################twitter#######################################################

    #For twitter
    # Get the list of all files and directories
    path = "twitter_csv/"
    dir_list = os.listdir(path)
    
    print("Files and directories in '", path, "' :")
    
    # prints all files
    #print(dir_list)
     
    username = request.user.username
    #print(username)
    filtered_lst=[]
    for element in dir_list:
        if username in element:
            filtered_lst.append(element)

    #print filtered file
    print(filtered_lst)

    dates =[]
    times =[]
    keywords =[]
    link = []
    path = []
    


    for file in filtered_lst:
        date = file.split("-")[0].replace('_','/')
        dates.append(date)
        time = file.split("-")[1].replace('_',':')
        times.append(time)
        keyword= file.split("-")[2]
        keywords.append(keyword)
        downloadpath = file
        print("path:",downloadpath)
        path.append('/'+'tw_dashbaord/'+downloadpath)
        link.append('http://103.101.197.155:1082/twitter/download/' +file)
        print('http://103.101.197.155:1082/twitter/download/' +file)
        

    print(dates, times, keywords, link)
    sl=list(range(1,len(keywords)+1)) 
    print(sl)   

    
    
    df = pd.DataFrame(
    {'SL' : sl,
     'keywords' : keywords,
     'times':times,
     'dates':dates,
     'link' :link,
     'path' :path
    })
    print(df)  
    json_records = df.reset_index().to_json(orient ='records')
    data_1 = []
    data_1 = json.loads(json_records)

################################################Google#######################################################
#For twitter
    # Get the list of all files and directories
    path = "google_csv/"
    dir_list = os.listdir(path)
    
    print("Files and directories in '", path, "' :")
    
    # prints all files
    #print(dir_list)
     
    username = request.user.username
    #print(username)
    filtered_lst=[]
    for element in dir_list:
        if username in element:
            filtered_lst.append(element)

    #print filtered file
    print(filtered_lst)

    dates =[]
    times =[]
    keywords =[]
    link = []
    path =[]
    


    for file in filtered_lst:
        date = file.split("-")[0].replace('_','/')
        dates.append(date)
        time = file.split("-")[1].replace('_',':')
        times.append(time)
        keyword= file.split("-")[2]
        keywords.append(keyword)
        downloadpath = file
        print("path:",downloadpath)
        path.append('/'+'gl_dashbaord/'+downloadpath)
        link.append('http://103.101.197.155:1082/google/download/' +file)
        print('http://103.101.197.155:1082/google/download/' +file)
        

    print(dates, times, keywords, link)
    sl=list(range(1,len(keywords)+1)) 
    print(sl)   

    
    
    df = pd.DataFrame(
    {'SL' : sl,
     'keywords' : keywords,
     'times':times,
     'dates':dates,
     'link' :link,
     'path' :path
    })
    print(df)  
    json_records = df.reset_index().to_json(orient ='records')
    data_2 = []
    data_2 = json.loads(json_records)


################################################YouTube#######################################################
    #For YouTube
    # Get the list of all files and directories
    path = "youtube_csv/"
    dir_list = os.listdir(path)
    
    print("Files and directories in '", path, "' :")
    
    # prints all files
    #print(dir_list)
     
    username = request.user.username
    #print(username)
    filtered_lst=[]
    for element in dir_list:
        if username in element:
            filtered_lst.append(element)

    #print filtered file
    print(filtered_lst)

    dates =[]
    times =[]
    keywords =[]
    link = []
    path =[]
    


    for file in filtered_lst:
        date = file.split("-")[0].replace('_','/')
        dates.append(date)
        time = file.split("-")[1].replace('_',':')
        times.append(time)
        keyword= file.split("-")[2]
        keywords.append(keyword)
        downloadpath = file
        print("path:",downloadpath)
        path.append('/'+'yt_dashbaord/'+downloadpath)
        link.append('http://103.101.197.155:1082/youtube/download/' +file)
        print('http://103.101.197.155:1082/youtube/download/' +file)
        

    print(dates, times, keywords, link)
    sl=list(range(1,len(keywords)+1)) 
    print(sl)   

    
    
    df = pd.DataFrame(
    {'SL' : sl,
     'keywords' : keywords,
     'times':times,
     'dates':dates,
     'link' :link,
     'path' :path
    })
    print(df)  
    json_records = df.reset_index().to_json(orient ='records')
    data_3 = []
    data_3 = json.loads(json_records)
    







    context = {'f': data, 't':data_1, 'g':data_2, 'y':data_3}
    print(context)
    


   
    return render(request, 'download.html',context)

@login_required
def facbook_download(request):
    # Get the list of all files and directories
    path = "facebook_csv/"
    dir_list = os.listdir(path)
    
    print("Files and directories in '", path, "' :")
    
    # prints all files
    #print(dir_list)
     
    username = request.user.username
    #print(username)
    filtered_lst=[]
    for element in dir_list:
        if username in element:
            filtered_lst.append(element)

    #print filtered file
    print(filtered_lst)
    for file in filtered_lst:
        link ='http://103.101.197.155:1082/facebook_posts/download/' +file
    return HttpResponseRedirect(link)

    

def analytics(request):
    return render(request, 'analytics.html')
    
    
